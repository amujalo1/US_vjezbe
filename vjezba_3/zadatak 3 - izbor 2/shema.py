import json

# JSON data
json_data = {
  "version": 1,
  "author": "Anonymous maker",
  "editor": "wokwi",
  "parts": [
    {
      "type": "board-pi-pico-w",
      "id": "pico",
      "top": 145.15,
      "left": -39.75,
      "rotate": 90,
      "attrs": { "env": "micropython-20231227-v1.22.0" }
    },
    {
      "type": "wokwi-membrane-keypad",
      "id": "keypad1",
      "top": -184.4,
      "left": -109.6,
      "attrs": {}
    },
    {
      "type": "wokwi-7segment",
      "id": "sevseg1",
      "top": 197.82,
      "left": 279.52,
      "attrs": { "digits": "4" }
    }
  ],
  "connections": [
    [ "keypad1:C4", "pico:GP2", "green", [ "v0" ] ],
    [ "keypad1:C3", "pico:GP3", "green", [ "v0" ] ],
    [ "keypad1:C2", "pico:GP4", "green", [ "v0" ] ],
    [ "keypad1:C1", "pico:GP5", "green", [ "v0" ] ],
    [ "pico:GP6", "keypad1:R4", "blue", [ "v-19.2", "h9.6" ] ],
    [ "keypad1:R3", "pico:GP7", "blue", [ "v28.8", "h-9.9" ] ],
    [ "keypad1:R2", "pico:GP8", "blue", [ "v19.2", "h-10" ] ],
    [ "keypad1:R1", "pico:GP9", "blue", [ "v9.6", "h-9.6" ] ],
    [ "sevseg1:A", "pico:GP10", "green", [ "v-28.8", "h-384" ] ],
    [ "sevseg1:B", "pico:GP11", "green", [ "v-28.8", "h-441.6" ] ],
    [ "sevseg1:C", "pico:GP12", "green", [ "v37.56", "h-489.6", "v-134.4", "h57.6", "v28.8" ] ],
    [ "sevseg1:D", "pico:GP13", "green", [ "v37.56", "h-470.4", "v-134.4", "h48" ] ],
    [ "sevseg1:E", "pico:GP14", "green", [ "v37.56", "h-460.79", "v-134.4", "h38.4" ] ],
    [ "sevseg1:F", "pico:GP15", "green", [ "v-28.8", "h-460.8" ] ],
    [ "sevseg1:G", "pico:GP16", "green", [ "v37.56", "h-480" ] ],
    [ "sevseg1:DIG1", "pico:GP17", "blue", [ "v-28.8", "h-211.19", "v124.8", "h-220.8" ] ],
    [ "sevseg1:DIG2", "pico:GP18", "blue", [ "v-28.8", "h-240", "v124.8", "h-211.2" ] ],
    [ "sevseg1:DIG3", "pico:GP19", "blue", [ "v-28.8", "h-249.6", "v124.8", "h-192" ] ],
    [ "sevseg1:DIG4", "pico:GP20", "blue", [ "v27.96", "h-441.6" ] ],
    [ "sevseg1:DP", "pico:GP21", "black", [ "v18.36", "h-403.2" ] ]
  ],
  "dependencies": {}
}


json_string = json.dumps(json_data, indent=2)

with open("Diagram_Vj3Zadatak3i2.json", 'w') as file:
    file.write(json_string)

# Print the JSON string
print(json_string)