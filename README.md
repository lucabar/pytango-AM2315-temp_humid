# PyTango AM2315 Tango Device Server
This will be a quick tutorial of how to <b>set up a <a class="reference external" href="https://learn.adafruit.com/am2315-encased-i2c-temperature-humidity-sensor">AM2315 temperature and humidity sensor</a></b> <b>on a Rapsberry Pi</b> and how to <b>get a Tango Device Server running</b>. Parts of this will work with the <a class="external reference" href="https://pytango.readthedocs.io/en/stable/quicktour.html">Quick Tour</a>, a PyTango documentation for a general setup. The following tutorial is written by and designed for absolute beginners that do not have a great background knowledge on Linux-based systems and servers. Therefore, the language used might be less professional but hopefully equally understandable.<bar>
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
<code>$ python3 AM2315.py
21.1
43.6</code>
</pre>
The output in your command line should return the measured temperature and humidity (see above).<br>

From this folder you now no longer need any other file than <em>AM2315.py</em>.

## Installing Tango on your Pi
<a class="external reference" href="https://tango-controls.readthedocs.io/en/latest/contents.html">Tango</a> can be installed <a class="reference external" href="https://tango-controls.readthedocs.io/en/latest/installation/tango-on-raspberry-pi.html#installation-without-database">without database</a> on the Pi because it can access the Tango Database from your main computer (e.g. VirtualMachine). To install without the database run the following one line command:
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
a window with Jive will open and you can create a Tango Device Server as described in the <a class ="reference external" href ="https://pytango.readthedocs.io/en/stable/quicktour.html#server">pytango-documentation</a>. A detailed description of the specific Tango DS for the <b>AM2315 sensor</b> can be found further on in this Readme. But first let us establish a connection between the Tango database on your Virtual Machine and your Rapsberry Pi.
    
## Connecting Pi to Tango Database on your Virtual Machine (VM)
When you have multiple devices like Rapsberry Pis in your experimental set up, you want all of them to access one and the same database. For this, the database would have to be centralized on one main computer (in this example a Virtual Machine running through <a class="reference external" href=https://www.virtualbox.org/>Oracle VM VirtualBox</a>).<bar>

In the top bar you have to navigate to <em>Devices>Network>Network settings</em>. There you select <em>Bridged Adapter</em> instead of <em>NAT</em> as your <em>attached to</em>-device and select under <em>name</em> the port where you are connected to the internet (in case of a Mac something like <em>en0:Wi-Fi (AirPort)</em>). You may loose internet connection in this session but it should be restored once you restart your VM. Now you have established a two way connection between your main OS and the VM.<bar>
    
The next step is to figure out where your Tango Database server address (i.e. TANGO_HOST) lies. The server address is set the first time you install Tango on your VM and can be checked via the following command:
<pre>
<code>$ echo $TANGO_HOST
sardana-playground:10000</code>
</pre>

To point the Pi to that address, you need to change/access two files:
<ul type="circle">
    <li>/etc/tangorc – change the TANGO_HOST-name to your address from the VM. In my case: TANGO_HOST=sardana-playground:10000</li>
    <li>~/.profile – paste the following at the end of the file: "export TANGO_HOST=sardana-playground:10000"</li>
</ul>

If you now check your TANGO_HOST on your Pi through the aforementioned <em>echo</em>-command, the Tango Database server address from your VM will show up. Now you should be able to start a Tango Device Server on your Pi. To test this, run the pre-installed test server called <em>TangoTest</em> with the instance <test> on your Pi:
<pre>
<code>$ /usr/lib/tango/TangoTest test
Ready to accept request</code>
</pre>
Now you are good to go and start your own Tango Device Server!

## Writing the actual Tango Device Server
