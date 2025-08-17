from __future__ import annotations

from dataclasses import dataclass, field

from js import document, HTMLDivElement
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.inventory import Inventory

@dataclass
class InventoryOverlay:
    inventory: "Inventory"
    active: bool = False
    overlay_div: HTMLDivElement = field(init=False)  # declare at class level

    def __post_init__(self):
        # Assign the overlay div AFTER the dataclass is created
        self.overlay_div = document.querySelector(".inventory-overlay")
        if not self.overlay_div:
            raise RuntimeError("Inventory overlay div not found in DOM")

        # Hide by default
        self.overlay_div.style.display = "none"

        # Fetch items
        self.items = self.inventory.return_all_items()

    def draw(self, canvas=None):
        if not self.active:
            self.overlay_div.style.display = "none"
            return
        else:
            self.overlay_div.style.display = "flex"

        container = self.overlay_div.querySelector(".inventory-items")
        if not container:
            return
        
        slots = container.querySelectorAll(".inventory-slot")

        items_list = list(self.items.items())  

        for idx, slot in enumerate(slots):
            slot.innerHTML = ""
            slot.style.background = "rgba(0,0,0,0.3)"  # default empty slot

            if idx < len(items_list):
                name, item_data = items_list[idx]
                img = document.createElement("img")
                img.src = item_data.image_url or None
                if not img.src:
                    slot.style.background = "lightgray"
                else:
                    img.style.width = "100%"
                    img.style.height = "100%"
                    img.style.objectFit = "contain"

                    slot.appendChild(img)
            else:
                slot.style.background = ""
