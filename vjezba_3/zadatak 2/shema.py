import json

# Define the JSON data
json_data = {
  "version": 1,
  "author": "Anonymous maker",
  "editor": "wokwi",
  "parts": [
    {
      "type": "board-pi-pico-w",
      "id": "pico",
      "top": 49.15,
      "left": 8.25,
      "rotate": 90,
      "attrs": { "env": "micropython-20231227-v1.22.0" }
    },
    {
      "type": "wokwi-7segment",
      "id": "sevseg1",
      "top": -61.38,
      "left": -56.48,
      "attrs": { "digits": "4" }
    },
    {
      "type": "wokwi-pushbutton",
      "id": "btn1",
      "top": -22.6,
      "left": 192,
      "attrs": { "color": "green" }
    },
    {
      "type": "wokwi-pushbutton",
      "id": "btn2",
      "top": 35,
      "left": 192,
      "attrs": { "color": "green" }
    },
    {
      "type": "wokwi-pushbutton",
      "id": "btn3",
      "top": 92.6,
      "left": 192,
      "attrs": { "color": "green" }
    },
    {
      "type": "wokwi-pushbutton",
      "id": "btn4",
      "top": 150.2,
      "left": 192,
      "attrs": { "color": "green" }
    }
  ],
  "connections": [
    [ "sevseg1:A", "pico:GP2", "green", [ "v-19.2", "h124.8", "v115.2", "h-19.2" ] ],
    [ "sevseg1:B", "pico:GP3", "green", [ "v-28.8", "h96", "v115.2", "h-57.6", "v48" ] ],
    [ "sevseg1:C", "pico:GP4", "green", [ "v18.36", "h48" ] ],
    [ "sevseg1:D", "pico:GP5", "green", [ "v27.96", "h57.6" ] ],
    [ "sevseg1:E", "pico:GP6", "green", [ "v37.56", "h48.01" ] ],
    [ "sevseg1:G", "pico:GP8", "green", [ "v47.16", "h-9.6" ] ],
    [
      "sevseg1:F",
      "pico:GP7",
      "green",
      [ "v-28.8", "h0", "v-9.6", "h134.4", "v163.2", "h-115.2" ]
    ],
    [ "sevseg1:DP", "pico:GP9", "green", [ "v0" ] ],
    [ "sevseg1:DIG1", "pico:GP10", "blue", [ "v-9.6", "h-76.79", "v124.8", "h86.4" ] ],
    [ "sevseg1:DIG2", "pico:GP11", "blue", [ "v-28.8", "h-115.2", "v153.6", "h76.8" ] ],
    [ "sevseg1:DIG3", "pico:GP12", "blue", [ "v-48", "h-134.4", "v182.4", "h76.8" ] ],
    [ "sevseg1:DIG4", "pico:GP13", "blue", [ "v8.76", "h-76.8" ] ],
    [ "pico:GND.1", "btn2:2.r", "black", [ "v-28.8", "h144" ] ],
    [ "btn1:2.r", "pico:GND.1", "black", [ "h0.2", "v19.4", "h-76.8", "v57.6", "h-67.2" ] ],
    [ "btn3:2.r", "pico:GND.1", "black", [ "h0.2", "v19.4", "h-76.8", "v-57.6", "h-67.2" ] ],
    [ "btn4:2.r", "pico:GND.1", "black", [ "h0.2", "v19.4", "h-76.8", "v-115.2", "h-67.2" ] ],
    [ "btn1:1.r", "pico:GP18", "gold", [ "v0", "h29", "v240", "h-278.4" ] ],
    [ "btn2:1.r", "pico:GP19", "gold", [ "v0", "h19.4", "v172.8", "h-288" ] ],
    [ "btn3:1.r", "pico:GP20", "gold", [ "v0", "h38.6", "v134.4", "h-288" ] ],
    [ "btn4:1.r", "pico:GP21", "gold", [ "v0", "h48.2", "v86.4", "h-288" ] ]
  ],
  "dependencies": {}
}

# Convert the JSON data to a string
json_string = json.dumps(json_data, indent=2)

with open("Diagram_Vj3Zadatak2.json", 'w') as file:
    file.write(json_string)

# Print the JSON string
print(json_string)
