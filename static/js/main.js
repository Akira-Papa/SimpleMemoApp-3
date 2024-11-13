// Handle edit memo
function editMemo(id) {
    const memoCard = document.querySelector(`#memo-${id}`);
    const title = memoCard.querySelector('.memo-title').textContent;
    const content = memoCard.querySelector('.memo-content').textContent;
    
    document.querySelector('#editMemoForm').action = `/memo/${id}/edit`;
    document.querySelector('#editMemoTitle').value = title;
    document.querySelector('#editMemoContent').value = content;
    
    new bootstrap.Modal(document.querySelector('#editMemoModal')).show();
}

// Handle delete confirmation
function confirmDelete(id) {
    if (confirm('このメモを削除してもよろしいですか？')) {
        document.querySelector(`#deleteMemoForm-${id}`).submit();
    }
}

// Handle search input
document.querySelector('#searchInput').addEventListener('input', function(e) {
    const searchForm = document.querySelector('#searchForm');
    if (e.target.value.length === 0) {
        searchForm.submit();
    }
});

// Initialize Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
