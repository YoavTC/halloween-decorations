# Destroy the decoration
kill @e[type=armor_stand,distance=..1.2]
kill @e[type=minecraft:block_display,distance=..1.2]
kill @e[type=minecraft:item_display,distance=..1.2]
kill @e[type=minecraft:text_display,distance=..1.2]
kill @e[type=minecraft:interaction,distance=..1.2]
kill @s

scoreboard players add count decoplus.old 1