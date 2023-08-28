function changeStatus(categoryId) {
    const url = `/admin/events/eventcategory/${categoryId}/change_status/`;
    const xhr = new XMLHttpRequest();
    xhr.open('POST', url);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.status === 200) {
            location.reload();  // Refresh the page after successful status change
        }
    };
    xhr.send();
}
