// Generated by CoffeeScript 1.3.3
(function() {
  var Map;

  Map = (function() {

    function Map(opts) {
      this.context = opts.context;
      this.position = opts.position;
      this.squareHeight = opts.squareHeight;
      this.canvas = opts.canvas;
      this.format = 9;
      this.fillStyle = "rgba(255, 255, 255, 0)";
      this.strokeStyle = "red";
      this.strokeWidth = 0;
      this.width = (this.format + 1) * this.squareHeight;
      this.height = (this.format + 1) * this.squareHeight;
      this.draw();
    }

    Map.prototype.draw = function() {
      var column, line, x, y, _i, _ref, _results;
      this.context.fillStyle = this.fillStyle;
      this.context.strokeStyle = this.strokeStyle;
      this.context.lineWidth = this.strokeWidth;
      _results = [];
      for (line = _i = 0, _ref = this.format; 0 <= _ref ? _i <= _ref : _i >= _ref; line = 0 <= _ref ? ++_i : --_i) {
        _results.push((function() {
          var _j, _ref1, _results1;
          _results1 = [];
          for (column = _j = 0, _ref1 = this.format; 0 <= _ref1 ? _j <= _ref1 : _j >= _ref1; column = 0 <= _ref1 ? ++_j : --_j) {
            x = line * this.squareHeight + this.position.left;
            y = column * this.squareHeight + this.position.top;
            this.context.beginPath();
            this.context.rect(x, y, this.squareHeight, this.squareHeight);
            _results1.push(this.context.fill());
          }
          return _results1;
        }).call(this));
      }
      return _results;
    };

    return Map;

  })();

  window.Map = Map;

}).call(this);
