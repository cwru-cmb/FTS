# FTS

This is code to run the original FTS, built long ago by Eric Torbet, currently using a Velmex linear stage.

Relevant info:
- The focal length of the FTS parabolic mirror (if that's installed) is 24”. The distance from focusing mirror to the top of the FTS is something like 13.5”
- As the mirror moves at velocity $v$, the optical path length varies as $\2v$, so the phase at a wavelength $\lambda$ varies as $\phi(t) = 2 \pi \cdot 2 v t / \lambda$.
  Thus, the signal, looks like $\cos{\phi(t)} = \cos{ 2\pi 2 v t/\lambda }$  From this we can see that the detector modulation signal frequency is $f = 2 v / \lambda = 2 v \nu/c$.
  This allows us to convert from the frequency bin of a detector FFT to a photon frequency using $\nu = f c / (2 v)$.

Notes, I think from Allen Foster:

Moving the Mirror: 
- Plug in the stage controller to the outlet and the computer. Make sure the controller box is TURNED ON!!! 
- The control code is called “VXM_controller.py”
- Open an Ipython session in the home dir. Import the script, for example if we import VXM_controller as v, then to open the connection and ‘home’ the stage, use
		v.VXM_online(port=portname)
 - The code uses ‘sudo’ to make sure the port is read/write by users, so you are required to enter the password
 - The script will display “opened successfully” but will hang until the stage is centered at position 0.

- To get the position at any time you may enter v.VXM_get_position(‘print’)
 - v.show_pos() to update position, but it does so in a loop forever and doesn't close the serial port when you control-c out of it.
- To tell the stage to move to position ‘pos’ enter v.VXM_to_position(pos)... pos may be positive or negative (-77 is furthest from grid, 77 is closest). I generally start the FTS scans from position -77.

To perform the scans, you can use scanset:	
- v.scanset(direction, speed, distance, n)	
 - Where speed is in [mm/s] distance is in [mm] and direction is ‘+’ or ‘-’.
- If starting from position -77, then you will use: v.scanset(‘+’,2,154,20)  
to scan in positive direction at a speed of 2 mm/s for 154 mm, 
then come back and repeat 20 times (one scan is up AND back).
	
TROUBLESHOOTING!
- Make sure the controller box is powered on.
- Plug the usb into the computer (I just had trouble on icecontrol while using the usb port with the little lightning bolt symbol… so I’d stick w the blue USB3.0 ports)

- If you get “ValueError: invalid literal for int() with base 10: 'X+0000000\r'”, I think this means that the controller is not communicating with the stage, i.e. the buffer is empty. You may try the following:
 - v.ser.close()
 - v.VXM_online()
- Check to make sure that the stage is actually moving. If not, try closing ipython and restarting. If v.VXM_online() doesn’t move the stage again, try unplugging the USB and plugging into a new port. Then do the above two commands again. Listen for stage motion during the homing.

If that doesn’t work close the ipython session again. Unplug the USB, turn off the controller and restart the process (i.e. turn on controller, plug in usb and open ipython session etc..)
