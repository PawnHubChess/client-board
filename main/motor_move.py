import time
from threading import Thread
from motor import Motor
from miscellaneous.units import Units
from miscellaneous.pins import Pins
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass

pins = Pins()
units = Units()

motorX = Motor('motorX', pins.STEP_X, pins.DIR_X, pins.EN_X)
motorY = Motor('motorY', pins.STEP_Y, pins.DIR_Y, pins.EN_Y)

class Motor_move:
    def move_motor_on_board(dif_x, dif_y, units):
        try:
            # Knight Movement
            travelFieldsX = units.fieldSteps * abs(dif_x)
            travelFieldsY = units.fieldSteps * abs(dif_y)
            
            if (dif_x == 2) and (dif_y == 1):
                motorY.step((travelFieldsY / 2), 'cw', units.usDelay)
                motorX.step(travelFieldsX, 'cw', units.usDelay)
                motorY.step((travelFieldsY / 2), 'cw', units.usDelay)
            
            elif (dif_x == 1) and (dif_y == 2):
                motorX.step((travelFieldsX / 2), 'cw', units.usDelay)
                motorY.step(travelFieldsY, 'cw', units.usDelay)
                motorX.step((travelFieldsX / 2), 'cw', units.usDelay)

            elif (dif_x == -2) and (dif_y == 1):
                motorY.step((travelFieldsY / 2), 'cw', units.usDelay)
                motorX.step(travelFieldsX, 'ccw', units.usDelay)
                motorY.step((travelFieldsY / 2), 'cw', units.usDelay)

            elif (dif_x == -1) and (dif_y == 2):
                motorX.step((travelFieldsX / 2), 'ccw', units.usDelay)
                motorY.step(travelFieldsY, 'cw', units.usDelay)
                motorX.step((travelFieldsX / 2), 'ccw', units.usDelay)

            elif (dif_x == 2) and (dif_y == -1):
                motorY.step((travelFieldsY / 2), 'ccw', units.usDelay)
                motorX.step(travelFieldsX, 'cw', units.usDelay)
                motorY.step((travelFieldsY / 2), 'ccw', units.usDelay)

            elif (dif_x == 1) and (dif_y == -2):
                motorX.step((travelFieldsX / 2), 'cw', units.usDelay)
                motorY.step(travelFieldsY, 'ccw', units.usDelay)
                motorX.step((travelFieldsX / 2), 'cw', units.usDelay)

            elif (dif_x == -2) and (dif_y == -1):
                motorY.step((travelFieldsY / 2), 'ccw', units.usDelay)
                motorX.step(travelFieldsX, 'ccw', units.usDelay)
                motorY.step((travelFieldsY / 2), 'ccw', units.usDelay)

            elif (dif_x == -1) and (dif_y == -2):
                motorX.step((travelFieldsX / 2), 'ccw', units.usDelay)
                motorY.step(travelFieldsY, 'ccw', units.usDelay)
                motorX.step((travelFieldsX / 2), 'ccw', units.usDelay)
                
            else: 
                # Non-Knight Movement
                if dif_x > 0:
                    def motorStepPosX(): # Move in postive X direction
                        motorX.step(travelFieldsX, 'cw', units.usDelay)
                    Thread(target = motorStepPosX).start()

                elif dif_x < 0:
                    def motorStepNegX(): # Move in negative X direction
                        motorX.step(travelFieldsX, 'ccw', units.usDelay)
                    Thread(target = motorStepNegX).start()

                if dif_y > 0:
                    def motorStepPosY(): # Move in postive Y direction
                        motorY.step(travelFieldsY, 'cw', units.usDelay)
                    Thread(target = motorStepPosY).start()

                elif dif_y < 0:
                    def motorStepNegY(): # Move in negative Y direction
                        motorY.step(travelFieldsY, 'ccw', units.usDelay)
                    Thread(target = motorStepNegY).start()

                time.sleep((abs(dif_x) + abs(dif_y)) * 0.8)

        except KeyboardInterrupt:
            GPIO.output(motorX.EN, GPIO.HIGH)
            GPIO.output(motorY.EN, GPIO.HIGH)

    def manual_movement():
        move_x = int(input("Move fields in X direction: "))
        move_y = int(input("Move fields in Y direciton: "))

        Motor_move.move_motor_on_board(move_x, move_y, units)

# Motor_move.manual_movement()
