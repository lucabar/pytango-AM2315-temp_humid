# PyTango AM2315 Tango Device Server
This repository holds a Tango Device Server for the <a href = "https://www.adafruit.com/products/1293">AM2315 temperature and humidity sensor</a> and a quick tutorial on how it was written and what will be needed to get the Server running. I am working on a Raspberry Pi 4 with PyTango 9.2.5 (without database) but this tutorial should work with any hardware supporting an i2c bus. How to hook up the AM2315 to a Rapsi or another Arduino is shown <a href="https://cdn-learn.adafruit.com/downloads/pdf/am2315-encased-i2c-temperature-humidity-sensor.pdf?timestamp=1588759334">here</a>. <bar>

## Installing the AM2315 driver
Start by installing the <a href="https://github.com/adafruit/Adafruit_Blinka">Adafruit_Blinka library</a> that enables CircuitPython support and the <a href="https://github.com/adafruit/Adafruit_CircuitPython_AM2320">Adafruit CircuitPython AM2320 library</a> (there is so far only a C++ library for the AM23<b>15</b> whereas the AM23<b>20</b> Python library works just as well for our AM2315):

<pre>
<code>$ pip3 install adafruit-blinka
$ pip3 install adafruit-circuitpython-am2320</code>
</pre>

Now you should be able to <code class="code-colors inline">import adafruit_am2320</code> in a python prompt and test the driver.

## Registering the TangoDS and connecting databases
Because you will want to run and debug your Server while writing it, you first need to register it with the Tango Database. To register it on your hardware (here a Raspi), you have to point your TANGO_HOST-name to the database address on your main computer where the Tango database is installed. In case you have already done that you can skip the next abstract.

### Pointing to the main database
To give your Raspi (or other) access to the main data base you have to change two files:

<ul type="circle">
    <li>/etc/tangorc – change <em>TANGO_HOST=some_tango_host</em> to the database address from the main computer (let's say <em>my_tango_host</em>). If you do not know that address, run <code class ="code-colors inline">$echo $TANGO_HOST</code> on your database computer and you will get <em>my_tango_host</em>.</li>
    <li>~/.profile – paste the following at the end of the file: "export TANGO_HOST=my_tango_host"</li>
</ul>

### Registering TangoDS
You will probably know from the <a href="https://pytango.readthedocs.io/en/stable/quicktour.html">PyTango documentation</a> that a TDS will need a name (<em>ServerName</em>) and an instance (<em>Instance</em>) on which it can be called. Furthermore it needs to know which class (<em>Class</em>) inside its code is the TangoClass; this TangoClass name is usually the same as the ServerName because there usually is not more than one TangoClass active on one server. Lastly you will need to name your device (<em>Instance/tango_device_server/1</em>) with which the client will talk to the server. The <em>tango_device_server</em> will be the file with the actual server code but without the extension (here: temp_humid), the <em>Instance</em> will be the same as the one from the Server-name and the digit in the end is just to organize possible multiple connected devices (can also be a string).<bar>
The registration can be done via the <b>Jive</b> GUI or manually inside a python console. A test instance for the AM2315 Tango Device Server could be registered through:

<pre>
<code>>>> import tango
>>> my_device = tango.DbDevInfo()
>>> my_device.server = "TempHumid/test"
>>> my_device.class = "TempHumid"
>>> my_device.name = "test/temp_humid/1"

>>> db = tango.Database()
>>> db.add_device(my_device)</code>
</pre>
## Writing the actual Tango Device Server
The main part of the <b>Tango Device Server</b> is made up by the <b>TangoClass</b> (here <em>TempHumid</em>). It is a python class that inherits from the <code class="code-colors inline">tango.server.Device</code> class. One important method the TangoClass inherits is the <em>init_device</em> method. It initializes an object for the class itself (<code class="code-colors inline">Device.init_device(self)</code>) and one as an object of the AM2320 driver class (<code class ="code-colors inline">self.am2315=am_driver.AM2315</code>). These initializations are run inside a try-except environment so that an error can be thrown if the connection of computer and sensor is faulty.  

Furthermore, the <b>attributes</b> are defined
<pre>
<code>self.temp = 0
self.humid = 0</code>
</pre>  
These attributes will later get changed by commands and then called up by a client (Jive, python console etc.).
An attribute has <b>attribute properties</b> such as a <em>name, unit, dtype, doc</em> and many more. These properties help both the Server and the User understand the attribute in question and even set warning/alarm limits.  

Next there are <b>commands</b> that can be executed by the clients. Here we have three important ones. <code class="code-colors inline">get_data</code>: Getting the temperature and humidity of the AM2320 object (<em>self.am2315</em>) and then saving this object's temperature and humidity as the one of the TangoClass object (<em>self.temp/self.humid</em>) itself. Up until now there is no output, we are just getting values from the AM2315 sensor with which we are updating the TempHumid-attributes <em>self.temp</em> and <em>self.humid</em>. The <em>get_data</em> command is only being executed when a client asks for it. It could also be executed regularly (<em>polling</em>, see PyTango documentation) to be independent of the client requests. How often is being measured can be controlled thorugh <em>polling</em> (PyTango documentation).  
    
When a client asks for the temperature or humidity, the <code class="code-colors inline">get_temperature, get_humidity</code> commands are executed. They return the value that is currently saved as the attribute <em>temperature</em>. Usually naming methods is up to the coder but in the case of a TangoClass it is important that for each attribute there is one method that can <b>read</b> the attribute. To ensure this, the reading method has to be called <em>read_attribute(self)</em> (here <em>read_temperature</em>) or when named otherwise, be specified by the attribute property <em>fget</em>.  
    
Furthermore, there are some additional logging operators that can make the debugging and error handling easier. They decide which command will be documented in the output and whether input, output or arguments will be returned. When running the Server, the debugging level can be specified by adding <code class="code-colors inline">-v1</code> (or 2,3,4 respectively, 4 being the debug and 1 the fatal error level) at the end of the line. The <em>tango.am2315_service</em> file in this repository in turn regulates where the output will be stored (using journalctl).  
    
Lastly, the <code class ="code-colors inline">run.server()</code> method, inherited from the <code class="code-colors inline">tango.server.Device</code> class, will be executed to start the whole Server process.  
    
## Running the TangoDS

To get the TangoDS running, make sure you are connected to your main Tango database as described above and also make sure that the Server file (here temp_humid.py) is made an executable. Now navigate to where the file is located and run
<pre>
<code>python3 TempHumid.py test -v4</code>
</pre>
The argument <em>test</em> here is the name of the <em>Instance</em> given to the Server in a chapter above. It should return
<pre>
<code>Ready to accept request</code>
</pre>
and maybe some logging decorators. <b>Congrats!</b> Your Server is now up and running and you can start adding clients in seperate terminal tabs.
