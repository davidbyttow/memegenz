
var INITIAL_TEXT_HEIGHT = 50;
var TEXT_STEP_SIZE = 5;
var MIN_TEXT_HEIGHT = 30;
var PADDING_X = 10;
var PADDING_Y = 10;
var MAX_LINES = 3;

function getQueryParam(name) {
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)");
  var results = regex.exec(window.location.search);
  return (results == null)
      ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function initFont(context) {
  context.fillStyle = '#FFF';
  context.font = INITIAL_TEXT_HEIGHT + 'px impact';
  context.strokeStyle = 'black';
  context.lineWidth = 2;
  context.textAlign = 'center';
  context.textBaseline = 'top';
}

function safeHandler(func) {
  return function() {
    try {
      func.apply(this, arguments);
    } catch (e) {
      console.error(e);
    }
    return false;
  };
}

function getUpperText() {
  return $('#editor-upper-text').val();
}

function getLowerText() {
  return $('#editor-lower-text').val();
}

function isListed() {
  return !$('#unlist-meme-checkbox').prop('checked');
}

function CanvasEditor(canvasEl) {
  this.canvasEl = canvasEl;
  this.context = this.canvasEl.getContext('2d');
  this.templateName = getQueryParam('template_name');
  this.lastUpperText = '';
  this.lastLowerText = '';
  this.image = null;

  var image = new Image();
  var self = this;
  image.onload = function() {
    self.canvasEl.height = image.height;
    self.canvasEl.width = image.width;
    self.image = image;
    self.draw();
  };
  image.src = '/template/image/' + this.templateName;

  this.drawImpact = function(text, x, y) {
    this.context.fillText(text, x, y);
    this.context.strokeText(text, x, y);
  };

  this.countLines = function(words, maxWidth) {
    var lines = 1;
    var line = '';
    for (var i = 0; i < words.length; ++i) {
      var metrics = this.context.measureText(line + words[i]);
      var lineWidth = metrics.width;
      if (lineWidth > maxWidth) {
        ++lines;
        line = '';
      }
      line += words[i] + ' ';
    }
    return lines;
  }

  this.drawText = function(text, y, alignBottom) {
    if (!text) {
      return;
    }

    initFont(this.context);
    var x = this.canvasEl.width / 2;
    var maxWidth = this.canvasEl.width - (PADDING_X * 2);
    var words = text.split(' ');

    // First count the number of lines we need in order to select
    // an ideal font size.
    var lines = this.countLines(words, maxWidth);

    // Setup font sizes based on initial line count
    lineHeight = INITIAL_TEXT_HEIGHT - TEXT_STEP_SIZE * (lines - 1);
    lineHeight = Math.max(lineHeight, MIN_TEXT_HEIGHT);
    this.context.font = lineHeight + 'px impact';
    if (alignBottom) {
      this.context.textBaseline = 'bottom';
    }

    // Recount to get actual size for the offset.
    lines = this.countLines(words, maxWidth);
    if (alignBottom) {
      y -= lineHeight * (lines - 1);
    }

    // Now draw the actual lines.
    var line = '';
    for (var i = 0; i < words.length; ++i) {
      var metrics = this.context.measureText(line + words[i]);
      var lineWidth = metrics.width;
      if (lineWidth > maxWidth) {
        this.drawImpact(line, x, y);
        y += lineHeight;
        line = '';
      }
      line += words[i] + ' ';
    }
    if (line) {
      this.drawImpact(line, x, y);
    }
  };
  
  this.drawUpperText = function() {
    var text = getUpperText().toUpperCase();
    this.drawText(text, PADDING_Y);
    this.lastUpperText = text;
  };
  
  this.drawLowerText = function() {
    var text = getLowerText().toUpperCase();
    this.drawText(
      text, this.canvasEl.height - PADDING_Y, true);
    this.lastLowerText = text;
  };
  
  this.draw = function() {
    if (!this.image) {
      return;
    }
    this.context.drawImage(this.image, 0, 0);
    this.drawUpperText();
    this.drawLowerText();
  };

  this.getDataUrl = function() {
    return this.canvasEl.toDataURL('image/png');
  }
}

function initEditor() {
  var canvasEl = document.getElementById('meme-canvas');
  if (!canvasEl) {
    return;
  }

  var canvasEditor = new CanvasEditor(canvasEl);
  
  $("#editor-upper-text").keyup(function() {
    canvasEditor.draw();
  });
  
  $("#editor-lower-text").keyup(function() {
    canvasEditor.draw();
  });

  $('#create-meme-button').click(safeHandler(function() {
    var dataUrl = canvasEditor.getDataUrl();
    $.post('/meme/image', {
      upper_text: getUpperText(),
      lower_text: getLowerText(),
      listed: isListed(),
      template_name: canvasEditor.templateName,
      image_data: dataUrl
    }, function(data) {
      window.location = '/meme/' + data.id
    }, 'json');
  }));
}

function initControls() {
  $('.id-create-meme').click(safeHandler(function() {
    window.location = '/templates';
  }));

  $('.id-delete-meme').click(safeHandler(function() {
    var id = $(this).attr('data-id');

    // TODO(d): Ask for confirmation.
    var result = confirm("Delete this meme?");
    if (!result) {
      return;
    }
    
    // TODO(d): Use DELETE semantics
    $.post('/meme/delete/' + id, {},
    function(data) {
      window.location = '/memes?order=recent';
    }, 'json');
  }));

  $('.id-create-meme-from-template').click(safeHandler(function() {
    var id = $(this).attr('data-id');
    window.location = '/meme?template_name=' + id;
  }));

  $('.id-template-name-box').on("keydown", function(e) {
    return e.which != 32;
  });

  $('.id-timestamp').each(function() {
    var ms = parseInt($(this).text());
    var date = new Date(ms);
    $(this).text(
        date.getMonth() + 1 + '/' + date.getDate() + '/' + date.getFullYear());
  });
}

$(function() {
  initEditor();
  initControls();
});