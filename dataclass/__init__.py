from dataclasses import dataclass


@dataclass
class datagroup:
    id_group: int


datagroup.id_group = int(open("group_id.txt", "r").read())
