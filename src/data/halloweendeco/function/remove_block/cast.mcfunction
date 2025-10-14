execute if block ~ ~ ~ #halloweendeco:player_head{components:{"minecraft:custom_data":{deco:1b}}} run return run setblock ~ ~ ~ air
execute if entity @s[distance=10..] run return fail

execute positioned ^ ^ ^.2 run function halloweendeco:remove_block/cast