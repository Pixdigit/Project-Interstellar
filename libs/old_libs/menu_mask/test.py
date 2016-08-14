# -*- coding: utf-8 -*-

import mask
import pygame

pygame.init()

test_mask = mask.new_mask()

test_mask.add_slot(pygame.Rect(1, 1, 1, 1))
test_mask.add_slot(pygame.Rect(2, 1, 1, 1))
test_mask.add_group("Master", [2, 6])
test_mask.add_slot(pygame.Rect(3, 1, 1, 1), "Master")
test_mask.add_slot(pygame.Rect(4, 1, 1, 1))

test_mask.add_slot(pygame.Rect(5, 1, 1, 1), slot_id=3)
test_mask.add_slot(pygame.Rect(6, 1, 1, 1), slot_id=6)
test_mask.add_slot(pygame.Rect(10, 1, 1, 1), slot_id=10)
test_mask.add_slot(pygame.Rect(8, 1, 1, 1), slot_id=8)
test_mask.add_slot(pygame.Rect(2, 1, 1, 1), slot_id=2)

test_mask.add_group("Master", [1, 2, 3])
test_mask.add_group("Master2", [10, 7, 8])

print test_mask.slots
print test_mask.groups
