
function getQueryParam(name) {
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)");
  var results = regex.exec(window.location.search);
  if(results == null) {
    return "";
  } else {
    return decodeURIComponent(results[1].replace(/\+/g, " "));
  }
}

function CanvasEditor() {
  this.canvas = document.getElementById('meme-canvas');
  this.ctx = this.canvas.getContext('2d');
  this.templateName = getQueryParam('template_name');

  this.drawWrappedText = function(text, x, y, maxWidth, lineHeight) {
    var words = text.split(' ');
    var line = '';

    for (var i = 0; i < words.length; ++i) {
      var testLine = line + words[i] + ' ';
      var metrics = this.ctx.measureText(testLine);
      var testWidth = metrics.width;
      if (testWidth > maxWidth) {
        this.ctx.fillText(line, x, y);
        line = words[n] + ' ';
        y += lineHeight;
      } else {
        line = testLine;
      }
    }
    this.ctx.fillText(line, x, y);
  }
  
  this.drawUpperText = function() {
    var centerX = this.ctx.canvas.width / 2;
    var centerY = this.ctx.canvas.height / 2;
    
    var maxWidth = 200;
    var lineHeight = 25;
    var x = (this.ctx.canvas.width - maxWidth) / 2;
    var y = 60;

    this.ctx.fillStyle = '#FFF';
    this.ctx.font = '16pt impact';
    this.ctx.lineWidth = 10;
    this.ctx.textAlign = 'center';
    
    var text = $('#editor-upper-text').val().toUpperCase();
    this.drawWrappedText(text, x, y, maxWidth, lineHeight);
  }
  
  this.drawLowerText = function() {
    var centerX = this.ctx.canvas.width / 2;
    var centerY = this.ctx.canvas.height / 2;

    this.ctx.fillStyle = '#FFF';
    this.ctx.font = '40pt impact';
    this.ctx.lineWidth = 5;
    this.ctx.textAlign = 'center';

    this.drawWrappedText($('#editor-upper-text').val().toUpperCase(), centerX, this.ctx.canvas.height - 50);
  }
  
  this.draw = function() {
    if (!this.canvas.getContext) {
      return;
    }
    var img = new Image();
    var self = this;
    img.onload = function() {
      self.ctx.canvas.height = img.height;
      self.ctx.canvas.width = img.width;
      self.ctx.drawImage(img,0,0);        
      
      self.drawUpperText();
      self.drawLowerText();
    };
    img.src = '/template/image/' + self.templateName;
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
    return false;
  });
  
});