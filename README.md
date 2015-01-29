# live-editor-server #
Server that allows live-editor to communicate with the output canvas in a 
separate tab, window, browser, or device.

## Demo ##
After creating a program using the "Open Output Window" to see the changes
in another window.  You can also use the output URL in another winodw or
on another device.

- <a href="http://elite-clover-821.appspot.com/" target="_blank">demo</a>

## Implementation Details ##
The server is written in Python.  It uses Google App Engine to serve files and
the Channel API to ferry messages between demos/simple/index.html and
demos/simple/output.html.

The CSS for the live editor has been updated so that the editor takes up more of
the window.  The "Oh noes!" now appears above the editor as opposed to beside it.

![editor in Chrome](https://raw.github.com/kevinb7/live-editor-server/master/editor.png)

Here's a screenshot of the program above running in the iOS simulator:

![output in iPad simulator](https://raw.github.com/kevinb7/live-editor-server/master/output.png)


## Future Work ##
- do linting/error checking in an iframe embedded in index.html so that these 
  tasks can be done without output.html
- only send code to the server (and output.html) after linting/error checking
  has occurred
- inject code from the server into output.html on load so that the program runs
  right away (and can run without index.html)
- improve the touch API so that the variable "touch" is set correctly whenever
  a touch handler is called.  The "touches" dictionary should still be 
  available for users that want to do things with multiple touches at the same
  time.
- integrate into the Khan Academy server code so that users can load existing
  programs
- automated testing
- proper logging
- improve rendering quality on retina devices
