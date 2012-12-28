
function CanvasEditor() {
  this.canvas = document.getElementById('meme-canvas');
  this.ctx = this.canvas.getContext('2d');
  
  this.drawWrappedText = function(text, x, y, maxWidth, lineHeight) {
    var words = text.split(' ');
    var line = '';

    for(var n = 0; n < words.length; n++) {
      var testLine = line + words[n] + ' ';
      var metrics = this.ctx.measureText(testLine);
      var testWidth = metrics.width;
      if(testWidth > maxWidth) {
        this.ctx.fillText(line, x, y);
        line = words[n] + ' ';
        y += lineHeight;
      }
      else {
        line = testLine;
      }
    }
    this.ctx.fillText(line, x, y);
  }
  
  this.drawUpperText = function() {
    var center_x = this.ctx.canvas.width / 2;
    var center_y = this.ctx.canvas.height / 2;
    
    var maxWidth = 200;
    var lineHeight = 25;
    var x = (this.ctx.canvas.width - maxWidth) / 2;
    var y = 60;

    this.ctx.fillStyle  = '#FFF';
    this.ctx.font       = '16pt impact';
    this.ctx.lineWidth  = 10;
    this.ctx.textAlign  = 'center';
    
    var text = $('#editor-upper-text').val().toUpperCase();
    this.drawWrappedText(text, x, y, maxWidth, lineHeight);
  }
  
  this.drawLowerText = function() {
    var center_x = this.ctx.canvas.width / 2;
    var center_y = this.ctx.canvas.height / 2;

    this.ctx.fillStyle  = '#FFF';
    this.ctx.font       = '40pt impact';
    this.ctx.lineWidth  = 5;
    this.ctx.textAlign  = 'center';

    this.drawWrappedText($('#editor-upper-text').val().toUpperCase(), center_x, this.ctx.canvas.height - 50);
  }
  
  this.draw = function() {
    if (this.canvas.getContext){
      var img = new Image();   // Create new img element
      var self = this;
      img.onload = function(){
        self.ctx.canvas.height = img.height;
        self.ctx.canvas.width = img.width;
        self.ctx.drawImage(img,0,0);        
        
        self.drawUpperText();
        self.drawLowerText();
      };
      img.src = '/images/success_kid.jpg'; // Set source path 
    }
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
  
});