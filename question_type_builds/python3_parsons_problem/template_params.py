import json
__twigprefix__ = r"""{% macro global_extra(jumbled_code) %}
<!--
Code for use within the CodeRunner HTML UI to implement a Parsons
Problem question type.

Much of this code is derived from the jsparson project by Ihantola
and Karavirta, licensed as below.

-- Richard Lobb, August 2021.

jsparsons licence:
=================
The MIT License

Copyright (c) 2010- Petri Ihantola and Ville Karavirta

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
-->
<style>
/** Stylesheet for the puzzles */

.sortable-code {
    position: static;
    padding-left: 0px;
    margin-left: 2%;
    float: left;
    width: 94%;
    max-width: 700px;
}

.sortable-code ul {
    font-size: 90%;
    font-family: monospace;
    list-style: none;
    background-color: #efefff;
    padding-bottom: 10px;
    padding-left: 0;
    margin-left: 0;
    border: 1px solid #efefff;;
}
.sortable-code ul:empty {
  padding-bottom: 30px;
}
.sortable-code li, .sortable-code li:before, .sortable-code li:after {
  box-sizing: content-box;
}
ul.output {
    background-color: #FFA;
}
.sortable-code li {
    -moz-border-radius:10px;
    -webkit-border-radius:10px;
    border-radius: 10px;
    background-color: white;
    border:1px solid lightgray;
    padding:4px;
    padding-left:8px;
    margin-top: 4px;
    white-space: nowrap;
    overflow: hidden;
    cursor: move;
}
.sortable-code li:hover {
    overflow: visible;
}


</style>

<script>
require(['jquery', 'jqueryui'], function($, jqui) { 

    function turn_on_touch() {
        // Turn on touch functionality
        // Detect touch support

        /*!
        * jQuery UI Touch Punch 0.2.3
        *
        * Copyright 2011–2014, Dave Furfero
        * Dual licensed under the MIT or GPL Version 2 licenses.
        *
        * Depends:
        *  jquery.ui.widget.js
        *  jquery.ui.mouse.js
        */
        $.support.touch = 'ontouchend' in document;

        // Ignore browsers without touch support
        if (!$.support.touch) {
            return;
        }

      var mouseProto = $.ui.mouse.prototype,
          _mouseInit = mouseProto._mouseInit,
          _mouseDestroy = mouseProto._mouseDestroy,
          touchHandled;

        /**
        * Simulate a mouse event based on a corresponding touch event
        * @param {Object} event A touch event
        * @param {String} simulatedType The corresponding mouse event
        */
        function simulateMouseEvent (event, simulatedType) {

        // Ignore multi-touch events
        if (event.originalEvent.touches.length > 1) {
          return;
        }

        event.preventDefault();

        var touch = event.originalEvent.changedTouches[0],
            simulatedEvent = document.createEvent('MouseEvents');

        // Initialize the simulated mouse event using the touch event's coordinates
        simulatedEvent.initMouseEvent(
          simulatedType,    // type
          true,             // bubbles                    
          true,             // cancelable                 
          window,           // view                       
          1,                // detail                     
          touch.screenX,    // screenX                    
          touch.screenY,    // screenY                    
          touch.clientX,    // clientX                    
          touch.clientY,    // clientY                    
          false,            // ctrlKey                    
          false,            // altKey                     
          false,            // shiftKey                   
          false,            // metaKey                    
          0,                // button                     
          null              // relatedTarget              
        );

        // Dispatch the simulated event to the target element
        event.target.dispatchEvent(simulatedEvent);
        }

        /**
        * Handle the jQuery UI widget's touchstart events
        * @param {Object} event The widget element's touchstart event
        */
        mouseProto._touchStart = function (event) {

        var self = this;

        // Ignore the event if another widget is already being handled
        if (touchHandled || !self._mouseCapture(event.originalEvent.changedTouches[0])) {
          return;
        }

        // Set the flag to prevent other widgets from inheriting the touch event
        touchHandled = true;

        // Track movement to determine if interaction was a click
        self._touchMoved = false;

        // Simulate the mouseover event
        simulateMouseEvent(event, 'mouseover');

        // Simulate the mousemove event
        simulateMouseEvent(event, 'mousemove');

        // Simulate the mousedown event
        simulateMouseEvent(event, 'mousedown');
        };

        /**
        * Handle the jQuery UI widget's touchmove events
        * @param {Object} event The document's touchmove event
        */
        mouseProto._touchMove = function (event) {

        // Ignore event if not handled
        if (!touchHandled) {
          return;
        }

        // Interaction was not a click
        this._touchMoved = true;

        // Simulate the mousemove event
        simulateMouseEvent(event, 'mousemove');
        };

        /**
        * Handle the jQuery UI widget's touchend events
        * @param {Object} event The document's touchend event
        */
        mouseProto._touchEnd = function (event) {

        // Ignore event if not handled
        if (!touchHandled) {
          return;
        }

        // Simulate the mouseup event
        simulateMouseEvent(event, 'mouseup');

        // Simulate the mouseout event
        simulateMouseEvent(event, 'mouseout');

        // If the touch interaction did not move, it should trigger a click
        if (!this._touchMoved) {

          // Simulate the click event
          simulateMouseEvent(event, 'click');
        }

        // Unset the flag to allow other widgets to inherit the touch event
        touchHandled = false;
      };

      /**
       * A duck punch of the $.ui.mouse _mouseInit method to support touch events.
       * This method extends the widget with bound touch event handlers that
       * translate touch events to mouse events and pass them to the widget's
       * original mouse event handling methods.
       */
      mouseProto._mouseInit = function () {
        
        var self = this;

        // Delegate the touch handlers to the widget's element
        self.element.bind({
          touchstart: $.proxy(self, '_touchStart'),
          touchmove: $.proxy(self, '_touchMove'),
          touchend: $.proxy(self, '_touchEnd')
        });

        // Call the original $.ui.mouse init method
        _mouseInit.call(self);
      };

      /**
       * Remove the touch event handlers
       */
      mouseProto._mouseDestroy = function () {
        
        var self = this;

        // Delegate the touch handlers to the widget's element
        self.element.unbind({
          touchstart: $.proxy(self, '_touchStart'),
          touchmove: $.proxy(self, '_touchMove'),
          touchend: $.proxy(self, '_touchEnd')
        });

        // Call the original $.ui.mouse destroy method
        _mouseDestroy.call(self);
      };
    }; 
    
    turn_on_touch(); // Run the jquery ui touch code.
    
    // =====================================================
    //
    // Now the code based on jsparsons (see licence at top)
    // ----------------------------------------------------
    // =====================================================

    var MAX_INDENT = 7;
    
    // regexp used for trimming
    var trimRegexp = /^\s*(.*?)\s*$/;
    var translations = {
        en: {
            code_panel_label: 'Use drag and drop to reorder and indent the following code lines.',
        }
    };

    // =================================================================
    //
    // ParsonsCodeLine object definition
    // ---------------------------------
    //
    // Defines a line object skeleton with only code and indentation from
    // a code string of the problem definition string (see parseCode)
    // =================================================================
    var ParsonsCodeLine = function(codestring, widget, allow_indent) {
        this.widget = widget;
        this.code = "";
        this.indent = 0;
        if (codestring) {
            // Consecutive lines to be dragged as a single block of code have strings "\\n" to
            // represent newlines => replace them with actual new line characters "\n"
            this.code = codestring.replace(/#distractor\s*$/, "").replace(trimRegexp, "$1").replace(/\\n/g, "\n");
            if (allow_indent) {
                this.indent = (codestring.length - codestring.replace(/^\s+/, "").length) / 4;
                this.indent = Math.min(this.indent, MAX_INDENT);
            }
            this.id = widget.id_prefix + ParsonsCodeLine.next_id++;
        }
    };

    ParsonsCodeLine.next_id = 0; // Effectively a static variable of the 'class'.


    // =================================================================
    //
    // ParsonsWidget object definition
    // -------------------------------
    // Creates a parsons widget.
    // Init must be called after creating an object.
    //
    // ==================================================================
    var ParsonsWidget = function(options) {
        var defaults = {
            'incorrectSound': false,
            'x_indent': 35,
            'feedback_cb': false,
            'lang': 'en'
        };

        this.options = jQuery.extend({}, defaults, options);
        this.id_prefix = options.sortableId + 'codeline';
        if (translations.hasOwnProperty(this.options.lang)) {
            this.translations = translations[this.options.lang];
        } else {
            this.translations = translations['en'];
        }

        // translate code_panel_label
        if (!this.options.hasOwnProperty("code_panel_label")) {
            this.options.code_panel_label = this.translations.code_panel_label;
        }
    };

    // Parse a problem definition given as a string and returns 
    // a list of ParsonCodeLines.
    ParsonsWidget.prototype.parseCode = function(lines, allow_indent) {
        var lineList = [],
            lineObject,
            that = this;
        // Create line objects out of each codeline.
        // Fields in line objects:
        //   code: a string of the code, may include newline characters and 
        //     thus in fact represents a block of consecutive lines
        //   indent: indentation level.
        $.each(lines, function(index, item) {
            lineObject = new ParsonsCodeLine(item, that, allow_indent);
            // Initialize line object with code and indentation properties
            if (lineObject.code.length > 0) {
                // The line is non-empty, not just whitespace
                lineList.push(lineObject);
            }
        });

        return lineList;
    };

    ParsonsWidget.prototype.init = function(code_string) {
        // Set up the widget, given the code to be displayed as a
        // single string. 
        // Can't use jQuery to get element directly as it can't parse
        // the element ID properly due to ___textareaId___ macro.
        var lines = this.parseCode(code_string.split("\n"), true);
        var that = this;
        var sortableElement = document.getElementById(this.options.sortableId);
        var sortable = $(sortableElement);
        html = '<p>' + this.options.code_panel_label + '</p>' +
            this.codeLinesToHTML(lines, this.options.sortableId);
        
        sortable.html(html);

        this.manageDrags();
    };


    ParsonsWidget.prototype.calcIndent = function(leftDiff) {
        // Return the indent based on the pixel difference given.
        return Math.max(0, Math.round(leftDiff / this.options.x_indent));
    };

    ParsonsWidget.prototype.getCodeString = function(element_id) {
        // Extract and return the code from the DOM as a single string.
        var parent = document.getElementById(element_id);
        var codeLines = parent.childNodes;
        var code = "";
        codeLines.forEach(item => {
            var line = item.innerText.trim();
            var indent = parseInt(item.style.marginLeft, 10);
            indent = indent / this.options.x_indent;
            var newLine = " ".repeat(indent * 4) + line + '\n';
            code += newLine;
        });
        return code;
    };

    ParsonsWidget.prototype.getStudentCodeString = function() {
        // Return the lines of code as a single string.
        return this.getCodeString('ul-' + this.options.sortableId);
    };

    ParsonsWidget.prototype.displayError = function(message) {
        if (this.options.incorrectSound && $.sound) {
            $.sound.play(this.options.incorrectSound);
        }
        alert(message);
    };

    ParsonsWidget.prototype.setHTMLIndent = function(codelineID, indent) {
        var codeLine = $(document.getElementById(codelineID));
        codeLine.css("margin-left", this.cssIndent(indent));
    };

    ParsonsWidget.prototype.cssIndent = function(indent) {
        return this.options.x_indent * Math.min(MAX_INDENT, indent) + "px";
    };

    ParsonsWidget.prototype.codeLineToHTML = function(codeline) {
        var style = codeline.indent ? ' style="margin-left:' + this.cssIndent(codeline.indent) + '" ' : '';
        return '<li id="' + codeline.id + '" class="ace-highlight-code lang-py"' + style + '>' + codeline.code + '<\/li>';
    };


    ParsonsWidget.prototype.codeLinesToHTML = function(codeLines, destinationID) {
        // Construct and return a single <ul> element with the HTML
        // for the given list of lines as embedded LI elements. The UL
        // element's ID is destinationID.
        var lineHTML = [];
        codeLines.forEach(line => {
            lineHTML.push(this.codeLineToHTML(line));
        });
        return '<ul id="ul-' + destinationID + '">' + lineHTML.join('') + '</ul>';
    };

    ParsonsWidget.prototype.manageDrags = function() {
        // Set up the code pane as a sortable UI elements with drag
        // management for indentation. An annoying issue here is that
        // the ___textareaId___ macro produces IDs that jQuery cannot
        // handle, so we have to use getElementById everywhere.
        var that = this;
        var sortableElement = document.getElementById('ul-' + this.options.sortableId);
        var sortable = $(sortableElement).sortable({
            start: function(event, ui) {
             },
            stop: function(event, ui) {
                if ($(event.target)[0] != ui.item.parent()[0]) {
                    return;
                }
                // The helper isn't where it seems to be because of the margin!
                var currentMargin = parseInt(ui.item.css('margin-left'));
                var realPosition = currentMargin + ui.position.left - ui.item.parent().position().left;
                var indent = that.calcIndent(realPosition);
                that.setHTMLIndent(ui.item[0].id, indent);
            },
            grid: [this.options.x_indent, 1]
        });
        sortable.addClass("output");
    };
    
   window.ParsonsWidget = ParsonsWidget;
   
    function displayErrors(fb) {
        if(fb.errors.length > 0) {
            alert(fb.errors[0]);
        }
    } 

    $(document).ready(function() {
        var sortableId = 'sortable-___textareaId___';
        var crTextareaId = 'CR-parsons-code-___textareaId___';
        var parson = new ParsonsWidget({
            'sortableId': sortableId
        });

        var codeTextArea = document.getElementById(crTextareaId);

        var code = codeTextArea.value; // Extract the code as a single multiline string.
        parson.init(code);
        
        function sync_to_coderunner(mutations) {
            codeTextArea.value = parson.getStudentCodeString();
        };
        dropArea=document.getElementById('ul-' + sortableId);
        let observer=new MutationObserver(sync_to_coderunner);
        let observerOptions = {
            childList: true,
            attributes: true,
            characterData: false,
            subtree: false,
            attributeFilter: ['style'],
            attributeOldValue: false,
            characterDataOldValue: false
        };
        observer.observe(dropArea, observerOptions);
        if (window.ace && window.applyAceHighlighting) {
            window.applyAceHighlighting(window.ace, dropArea);
        }
    });
});
</script>

<html>
    <head>
        <title>Simple js-parsons example</title>
    </head>
    <body>
        <div id="sortable-___textareaId___" class="sortable-code">
        </div>
        <div style="clear:both;"></div>
        <div id="CRactual"  style="display: none;">
        <h2>Code Here:</h2>
<textarea id="CR-parsons-code-___textareaId___" name='CR-parsons-code' class="coderunner-ui-element" rows="10" cols="40">
{{ jumbled_code }}
</textarea>
        </div>
    </body>
</html>

{% endmacro %}
"""
print(json.dumps({'__twigprefix__': __twigprefix__}))
