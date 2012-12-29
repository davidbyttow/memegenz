
var INITIAL_TEXT_HEIGHT = 50;
var TEXT_STEP_SIZE = 5;
var MIN_TEXT_HEIGHT = 30;
var PADDING_X = 20;
var PADDING_Y = 20;
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
}

function CanvasEditor() {
  this.canvas = document.getElementById('meme-canvas');
  this.context = this.canvas.getContext('2d');
  this.templateName = getQueryParam('template_name');
  this.lastUpperText = '';
  this.lastLowerText = '';

  this.drawImpact = function(text, x, y) {
    this.context.fillText(text, x, y);
    this.context.strokeText(text, x, y);
  };

  this.drawText = function(text, y, alignBottom) {
    if (!text) {
      return;
    }

    initFont(this.context);

    var maxWidth = this.canvas.width - (PADDING_X * 2);

    // First count the number of lines we need in order to select
    // an ideal font size.
    var lines = 1;
    var words = text.split(' ');
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

    lineHeight = INITIAL_TEXT_HEIGHT - TEXT_STEP_SIZE * (lines - 1);
    lineHeight = Math.max(lineHeight, MIN_TEXT_HEIGHT);
    this.context.font = lineHeight + 'px impact';
    
    line = '';
    var x = this.context.canvas.width / 2;

    var offsetY = 0;
    if (alignBottom) {
      offsetY = -lineHeight * (lines - 1) / 2;
    } else {
      offsetY = lineHeight;
    }

    y += offsetY;

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
    var text = $('#editor-upper-text').val().toUpperCase();
    this.drawText(text, PADDING_Y);
    this.lastUpperText = text;
  };
  
  this.drawLowerText = function() {
    var text = $('#editor-lower-text').val().toUpperCase();
    this.drawText(
      text, this.canvas.height - PADDING_Y * 2, true);
    this.lastLowerText = text;
  };
  
  this.draw = function() {
    var img = new Image();
    var self = this;
    img.onload = function() {
      self.context.canvas.height = img.height;
      self.context.canvas.width = img.width;
      self.context.drawImage(img, 0, 0);

      self.drawUpperText();
      self.drawLowerText();
    };
    img.src = '/template/image/' + self.templateName;
  };

  this.contextetDataUrl = function() {
    return this.context.canvas.toDataURL('image/png');
  }
}

$(function() {
  var canvasEditor = new CanvasEditor();
  canvasEditor.draw();
  
  $("#editor-upper-text").keyup(function() {
    canvasEditor.draw();
  });
  
  $("#editor-lower-text").keyup(function() {
    canvasEditor.draw();
  });

  $('#editor-submit-button').click(function() {
    try {
      var dataUrl = canvasEditor.getDataUrl();

      $.post('/meme/image', {
        listed: true,
        template_name: canvasEditor.templateName,
        image_data: dataUrl
      }, function(data) {
        window.location = '/meme/' + data.id
      }, 'json');
    } catch (ignored) {}

    return false;
  });
  
});