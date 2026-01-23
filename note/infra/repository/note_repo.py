from note.domain.note import Note
from note.domain.repository.note_repo import INoteRepository

class NoteRepository(INoteRepository):
    def get_notes(
            self,
            user_id: str,
            page: int, 
            items_per_page: int,
    ) -> tuple[int, list[Note]]:
        raise NotImplementedError
    
    def find_by_id(self, user_id: str, id: str) -> Note:
        return NotImplementedError
    
    def save(self, user_id: str, note: Note) -> Note:
        return NotImplementedError
    
    def update(self, user_id: str, note: Note) -> Note:
        return NotImplementedError
    
    def delete(self, user_id:str, id:str):
        return NotImplementedError
    
    def delete_tags(self, user_id:str, id:str):
        return NotImplementedError
    
    def get_notes_by_tag_name(self, user_id: str, tag_name:str, page:int, items_per_page:int) -> tuple[int, list[Note]]:
        return NotImplementedError