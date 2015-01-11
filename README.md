# live-editor-server #
Server that allows live-editor to communicate with the output canvas in a 
separate tab, window, browser, or device.

## Demo ##
Make sure you sign in using the same user account when opening both links.  
It may take a little bit of time for the program to start running the output 
window.  If the editor is empty, that's okay... just write some code.  :)

- <a href="http://elite-clover-821.appspot.com/editor" target="_blank">editor</a>
- <a href="http://elite-clover-821.appspot.com/output" target="_blank">output</a>

## Implementation Details ##
The server is written in Python.  It uses Google App Engine to server files and
the Channel API to ferry messages between demos/simple/index.html and
demos/simple/output.html.

The CSS for the live editor has been updated so that the editor takes up more of
the window.  The "Oh noes!" now appears above the editor as opposed to beside it.

![editor in Chrome](https://raw.github.com/kevinb7/live-editor-server/master/editor.png)

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
