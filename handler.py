import pygame
from backend import *
import time as t
import asyncio
import aioconsole

pygame.init()
parser = InstructionParser()

#### REGISTERS ####

r0 = Register("R0", "16 bits")
r1 = Register("R1", "16 bits")
r1.value = 1.0
r2 = Register("R2", "16 bits")
r2.value = 2.0
r3 = Register("R3", "16 bits")
b = Register("B", "16 bits")
sp = Register("SP", "16 bits")
pc = Register("PC", "16 bits")

registers = {
    "r0": r0,
    "r1": r1,
    "r2": r2,
    "r3": r3,
    "b": b,
    "sp": sp,
    "pc": pc
}

#########################

#### REGISTER WINDOW ####

reg_positions = {
    60: r0,
    80: r1,
    100: r2,
    120: r3,
    140: b,
    160: sp,
    180: pc
}

width, height = 300, 600

reg_window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Register Window')
reg_window.fill((33, 33, 33))

title_font = pygame.font.SysFont(None, 48)
title = title_font.render('Registers:', True, (255, 255, 255))
reg_window.blit(title, (20, 20))

text_font = pygame.font.SysFont(None, 24)


async def run_console():
    while True:
        inst = await aioconsole.ainput("> ")
        if inst == "quit":
            quit()
        for i in parser.parse(tokenize(inst)):
            if i.type == "AddNode":
                pc.value += 1  # Increment the PC by 1 byte for the instruction
                left = registers[i.left].value
                right = registers[i.right].value
                result = float(left + right)
                registers[i.left].value = result
                pc.value += 1  # Increment the PC by 1 byte, 4 bits for each register
                # print("console", registers)
            elif i.type == "SubNode":
                pc.value += 1  # Increment the PC by 1 byte for the instruction
                left = registers[i.left].value
                right = registers[i.right].value
                result = float(left - right)
                registers[i.left].value = result
                pc.value += 1  # Increment the PC by 1 byte, 4 bits for each register
            await asyncio.sleep(0)


async def run_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        reg_window.fill((33, 33, 33))
        # reg_window.blit(title, (20, 20))

        for curr_reg in reg_positions:
            text = text_font.render(reg_positions[curr_reg].name + " : " + str(reg_positions[curr_reg].value), True,
                                    (255, 255, 255))
            reg_window.blit(text, (20, curr_reg))
        pygame.display.update()
        # print("window", registers)
        await asyncio.sleep(1 / 60)


async def main():
    tasks = [asyncio.create_task(run_console()), asyncio.create_task(run_window())]

    for task in tasks:
        await task


asyncio.run(main())
