
function getQueryParam(name) {
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)");
  var results = regex.exec(window.location.search);
  return (results == null)
      ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
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
    
    // var maxWidth = 200;
    // var lineHeight = 25;
    // var x = (this.ctx.canvas.width - maxWidth) / 2;
    // var y = 60;

    this.ctx.fillStyle = '#FFF';
    this.ctx.font = '40pt impact';
    this.ctx.strokeStyle = 'black';
    this.ctx.lineWidth = 5;
    this.ctx.textAlign = 'center';
    
    var text = $('#editor-upper-text').val().toUpperCase();
    this.drawWrappedText(
      text,
      centerX,
      50);
  }
  
  this.drawLowerText = function() {
    var centerX = this.ctx.canvas.width / 2;
    var centerY = this.ctx.canvas.height / 2;

    this.ctx.fillStyle = '#FFF';
    this.ctx.font = '40pt impact';
    this.ctx.strokeStyle = 'black';
    this.ctx.lineWidth = 5;
    this.ctx.textAlign = 'center';

    var text = $('#editor-lower-text').val().toUpperCase();
    this.drawWrappedText(
      text,
      centerX,
      this.ctx.canvas.height - 15);
  }
  
  this.draw = function() {
    var img = new Image();
    var self = this;
    img.onload = function() {
      self.ctx.canvas.height = img.height;
      self.ctx.canvas.width = img.width;
      self.ctx.drawImage(img, 0, 0);

      self.drawUpperText();
      self.drawLowerText();
    };
    img.src = '/template/image/' + self.templateName;
  }

  this.getDataUrl = function() {
    return this.ctx.canvas.toDataURL('image/png');
  }
}

$(function() {
  var canvasEditor = new CanvasEditor();
  canvasEditor.draw();
  
  $("#editor-upper-text").keypress(function() {
    canvasEditor.draw();
  });
  
  $("#editor-lower-text").keypress(function() {
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