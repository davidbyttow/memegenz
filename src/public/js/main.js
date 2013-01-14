
var INITIAL_TEXT_HEIGHT = 50;
var TEXT_STEP_SIZE = 5;
var MAX_TEXT_HEIGHT = 70;
var MIN_TEXT_HEIGHT = 30;
var PADDING_X = 10;
var PADDING_Y = 10;
var MAX_LINES = 3;


var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'];

function getDateString(date) {
  return MONTHS[date.getMonth()] + ' ' + date.getDate() + ', ' + date.getFullYear();
}

function getQueryParam(name) {
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)");
  var results = regex.exec(window.location.search);
  return (results == null)
      ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
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
  this.initialTextHeight = INITIAL_TEXT_HEIGHT;
  this.textStepSize = TEXT_STEP_SIZE;
  this.minTextHeight = MAX_TEXT_HEIGHT;
  this.minTextHeight = MIN_TEXT_HEIGHT;
  this.upperTextModifier = 0;
  this.lowerTextModifier = 0;

  var image = new Image();
  var self = this;
  image.onload = function() {
    self.canvasEl.height = image.height;
    self.canvasEl.width = image.width;
    self.image = image;
    self.initialTextHeight = Math.floor(image.height / 7);
    self.maxTextHeight = Math.floor(self.initialTextHeight * 1.4);
    self.minTextHeight = Math.floor(self.initialTextHeight * 0.6);
    self.textStepSize =  Math.floor((self.initialTextHeight - self.minTextHeight) / 4);
    self.draw();
  };
  image.src = '/template/image/' + this.templateName;

  this.initFont = function() {
    this.context.fillStyle = '#FFF';
    this.context.font = this.initialTextHeight + 'px impact';
    this.context.strokeStyle = 'black';
    this.context.lineWidth = 2;
    this.context.textAlign = 'center';
    this.context.textBaseline = 'top';
  }

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
      if (lineWidth > maxWidth && line) {
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

    this.initFont();
    var x = this.canvasEl.width / 2;
    var maxWidth = this.canvasEl.width - (PADDING_X * 2);
    var words = text.split(' ');

    // First count the number of lines we need in order to select
    // an ideal font size.
    var lines = this.countLines(words, maxWidth);

    // Setup font sizes based on initial line count
    lineHeight = this.initialTextHeight - this.textStepSize * (lines - 1);
    lineHeight += alignBottom ? this.lowerTextModifier : this.upperTextModifier;

    lineHeight = Math.max(lineHeight, this.minTextHeight);
    lineHeight = Math.min(lineHeight, this.maxTextHeight);
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
      if (lineWidth > maxWidth && line) {
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

function pollStream() {
  var date = $('.id-first-date').attr('data-date')
  $.get('/stream/poll', {
    'after': date,
  }, function (data) {
    if (data) {
      $('.id-meme-stream').prepend(data);
    }
    setTimeout(pollStream, 5000);
  }, 'html');
}

function initEditor() {
  var canvasEl = document.getElementById('meme-canvas');
  if (!canvasEl) {
    return;
  }

  var canvasEditor = new CanvasEditor(canvasEl);
  
  $('#editor-upper-text').keyup(function() {
    canvasEditor.draw();
  });
  
  $('#editor-lower-text').keyup(function() {
    canvasEditor.draw();
  });

  $('.id-inc-upper-text-button').click(safeHandler(function() {
    canvasEditor.upperTextModifier += canvasEditor.textStepSize;
    canvasEditor.draw();
  }));
  $('.id-dec-upper-text-button').click(safeHandler(function() {
    canvasEditor.upperTextModifier -= canvasEditor.textStepSize;
    canvasEditor.draw();
  }));
  $('.id-inc-lower-text-button').click(safeHandler(function() {
    canvasEditor.lowerTextModifier += canvasEditor.textStepSize;
    canvasEditor.draw();
  }));
  $('.id-dec-lower-text-button').click(safeHandler(function() {
    canvasEditor.lowerTextModifier -= canvasEditor.textStepSize;
    canvasEditor.draw();
  }));

  $('#create-meme-form').submit(function(e) {
    e.preventDefault();
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
    return false;
  });
}

function initControls() {
  $('#upload-template-form').submit(function (e) {
    var templateName = $('.id-template-name-box').val();
    if (!templateName) {
      $('.id-error').text('Template name required')
      e.preventDefault();
      return false;
    }
    var filepath = $('.id-template-file-box').val();
    if (!filepath) {
      $('.id-error').text('File required')
      e.preventDefault();
      return false;
    }
  });

  $('.id-plusone').click(safeHandler(function() {
    var id = $(this).attr('data-id');
    window.location = '/vote/' + id;
  }));

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

  $('.id-delete-template').click(safeHandler(function() {
    var templateName = $(this).attr('data-id');

    // TODO(d): Ask for confirmation.
    var result = confirm("Delete this template?");
    if (!result) {
      return;
    }
    
    // TODO(d): Use DELETE semantics
    $.post('/template/delete/' + templateName, {},
    function(data) {
      window.location = '/memes?order=recent';
    }, 'json');
  }));

  $('.id-create-meme-from-template').click(safeHandler(function() {
    var templateName = $(this).attr('data-id');
    window.location = '/templates';
  }));

  $('.id-template-name-box').on("keydown", function(e) {
    return e.which != 32;
  });

  $('.id-timestamp').each(function() {
    var ms = parseInt($(this).text());
    var date = new Date(ms);
    $(this).text(getDateString(date));
  });

  $('.id-meme-thumb').hover(function() {
    $(this).find('.id-plusone').fadeIn(200);
  }, function() {
    $(this).find('.id-plusone').fadeOut(200);
  });

  $('.id-select-template').change(function() {
    var templateName = $(this).val();
    if (templateName) {
      window.location = '/meme?template_name=' + templateName;
    }
  });

  $('.id-see-voters').click(safeHandler(function() {
    var id = $(this).attr('data-id')
    $.get('/voters/' + id, {}, function (data) {
      if (data) {
        $('.id-voters-container').html(data);
      }
    }, 'html');
  }));

  if ($('.id-meme-stream').size()) {
    pollStream();
  }
}

$(function() {
  initEditor();
  initControls();
});