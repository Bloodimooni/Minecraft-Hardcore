# Minecraft-Hardcore challenge automation
This is a python script, to automate the Challenge that Martincitopants did in his latest video: 
https://www.youtube.com/watch?v=CYBdxuGj0X4&amp;pp=ygUPbWFydGluY2l0b3BhbnRz

# Warning!
So far I have only been able to test it on Linux, since my Server is running it.
I will try it on windows as soon as possible, please hold tight.

# How to use it?

1. To start, you will need to install python3 
https://www.python.org/downloads/

2. You need to download the minecraft server files and agree to the Eula.

3. make a run script:

For Windows 'run.bat':

```java -Xmx2048M -Xms1024M -jar server.jar nogui```

save the file as .bat and you are good to go.

For Linux 'run.sh':

```java -Xmx2048M -Xms1024M -jar server.jar nogui```

you still need to make it executable in linux. 
Simply type "sudo chmod +x run.sh" in the terminal.


# Once you are setup

Simply put the python file in the same directory as your server and run it in a terminal using:
python hardcore.py on windows 
or
python3 hardocore.py on linux.

If you want to shutdown the Server, just press CTRL + C and the server will shut down and save everything.

Enjoy!
