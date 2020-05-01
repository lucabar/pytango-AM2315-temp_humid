# Pytango AM2315 Tango Device Server
This will be a quick tutorial of how to <b>set up a <a class="reference external" href="https://learn.adafruit.com/am2315-encased-i2c-temperature-humidity-sensor">AM2315 temperature and humidity sensor</a></b> <b>on a Rapsberry Pi</b> and how to <b>get a Tango Device Server running</b>.

## Connecting the sensor to your Pi
Connect
<ul type="circle">
    <li>red wire (sensor VIN) to the first pin in the left column (Pi 3V3 power outlet),</li>
    <li>the yellow wire (sensor SDA) to the pin below the red (2nd on the left, Pi SDA),</li>
    <li>the white wire (sensor SCL) to the pin below the yellow (3rd on the left, Pi SCL) and finally</li>
    <li>the black wire (Ground) to the Ground pin (5th on the left).</li>
</ul>
   Now your AM2315 can successfully communicate with your Pi.

## Setting up the AM2315 on your Pi
Firstly, the <b>Adafruit-Python library</b> must be installed on the Pi. To do this, follow the instructions in the <em>Install_circuitpython_lib_pi.txt</em> file in the enclosed <em>i2cpython</em> folder.<br>
After completing this you can run the following command inside the <em>i2cpython</em> directory to see whether your sensor has been connected and the libraries have been installed successfully:<br>
<pre>
  <code>$ python3 AM2315.py</code>
</pre>
<br>The output in you command line should return the measured temperature and humidity, something like this:<br>

&emsp;21.1<br>
&emsp;43.6<br>

From this folder you now no longer need any other file than <em>AM2315.py</em>.

## Installing Pytango on your Pi
Pytango can be installed without database on the Pi because it can access the Tango Database from your main computer (e.g. VirtualMachine). To install without the database run the following one line command:
<pre>
  <code>sudo apt install tango-starter tango-test liblog4j1.2-java</code>
</pre>
I suggest you to install <b>Jive</b> as well, since it is an easy to understand and navigate client GUI. Jive requires <em>openjdk-8-jre</em> but we have <openjdk-11-jre</em> installed. We will now remove the 11-version and install in its place the one jive requires:
<pre>
<code>sudo apt purge default-jre default-jre-headless
sudo apt purge openjdk-11-jre openjdk-11-jre-headless 
sudo apt install openjdk-8-jre openjdk-8-jre-headless
sudo apt install ca-certificates-java libreoffice-sdbc-hsqldb</code>
</pre>
Now we can easily install Jive by the following commands:
<pre>
<code>sudo apt install --assume-yes wget\
wget -c https://people.debian.org/~picca/libtango-java_9.2.5a-1_all.deb \
sudo dpkg -i ./libtango-java_9.2.5a-1_all.deb </code>
</pre>
 or choose another libtango-java library from <a class="reference external" href="https://people.debian.org/~picca">picca</a>.<bar>
Now if you try and run
<pre>
<code>$jive</code>
</pre>
a window with jive will open and you can create a server as described in the <a class ="reference external" href ="https://pytango.readthedocs.io/en/stable/quicktour.html#server">pytango-documentation</a>.
