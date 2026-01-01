from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from services.group_selection_service import GroupSelectionService


@inject
async def get_specialities(
    group_service: FromDishka[GroupSelectionService],
    **_: object,
) -> dict[str, list[tuple[int, str]]]:
    items = await group_service.get_all_specialities()
    return {
        "items": [(s.id, s.full_name) for s in items],
    }


@inject
async def get_courses(
    dialog_manager: DialogManager,
    group_service: FromDishka[GroupSelectionService],
    **_: object,
) -> dict[str, list[tuple[int, str]]]:
    speciality_id = dialog_manager.dialog_data["speciality_id"]
    courses = await group_service.get_courses_by_speciality(speciality_id)
    return {
        "items": [(c, f"{c} курс") for c in courses],
    }


@inject
async def get_streams(
    dialog_manager: DialogManager,
    group_service: FromDishka[GroupSelectionService],
    **_: object,
) -> dict[str, list[tuple[str, str]]]:
    speciality_id = dialog_manager.dialog_data["speciality_id"]
    course = dialog_manager.dialog_data["course"]
    streams = await group_service.get_streams_by_speciality_course(speciality_id, course)
    return {
        "items": [(s, f"Поток {s}") for s in streams],
    }


@inject
async def get_groups(
    dialog_manager: DialogManager,
    group_service: FromDishka[GroupSelectionService],
    **_: object,
) -> dict[str, list[tuple[int, str]]]:
    speciality_id = dialog_manager.dialog_data["speciality_id"]
    course = dialog_manager.dialog_data["course"]
    stream = dialog_manager.dialog_data["stream"]
    groups = await group_service.get_groups_by_structure(speciality_id, course, stream)
    return {
        "items": [(g.id, g.name) for g in groups],
    }


@inject
async def get_subgroups(
    dialog_manager: DialogManager,
    group_service: FromDishka[GroupSelectionService],
    **_: object,
) -> dict[str, list[tuple[int, str]]]:
    group_id = dialog_manager.dialog_data["group_id"]
    subgroups = await group_service.get_subgroups_by_group(group_id)
    return {
        "items": [(sg.id, sg.name) for sg in subgroups],
    }
