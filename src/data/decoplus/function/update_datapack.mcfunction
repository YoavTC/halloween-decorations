tellraw @a {text:"Removing old decorations...",color:"yellow"}
scoreboard objectives add decoplus.old dummy
scoreboard players set count decoplus.old 0

execute as @e[type=minecraft:interaction,tag=deco_triggerbox] positioned as @s run function decoplus:update/remove_old

schedule function decoplus:update/notify 1s