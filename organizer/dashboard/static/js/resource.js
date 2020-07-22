// toggle edit mode
const toggleEditMode = () => {
    var divs = document.getElementsByClassName('editDetailBtn');
    for (var i = 0; i < divs.length; i++) {

        let element = divs[i]
        if ( element.classList.contains('hidden')) {
            element.classList.remove('hidden')
        } else {
            element.classList.add('hidden')
        }
    }
} ;

const getToken = () => {
  return document.querySelector('#details-form > input').value;
};

// Add Task
const addTask = async (title, resource) => {
    const csrftoken = getToken();
    try {
    const res = await axios.post('/api/tasks/',
        { title, resource },
        { headers: { 'X-CSRFToken': csrftoken }}
        );
    const response = res.data;
    location.reload();
    // TODO append new task to list
    return response;
      } catch (e) {
        console.error(e);
      }
};

// Delete Task
const deleteTask = async (taskId) => {
    const csrftoken = getToken();
    try {
        const res = await axios.delete('/api/tasks/'+ String(taskId) + '/',
            { headers: { 'X-CSRFToken': csrftoken }}
            );
        const response = res.data;
        // Todo remove from dom
        location.reload();
        return response;
    } catch (e) {
        console.error(e);
    }
};


// send post request to update resource
const updateResourcePost = async (payload, resourceId) => {
    const csrftoken = getToken();
    try {
    const res = await axios.patch('/api/resources/' + resourceId + '/',
        payload,
        { headers: { 'X-CSRFToken': csrftoken }}
        );
    const response = res.data;
    // TODO (?) Alert that resource was updated
    return response;
      } catch (e) {
        console.error(e);
      }
};


// Delete Resource
const deleteResource = async (resourceId) => {
    const csrftoken = getToken();
    try {
    const res = await axios.delete('/api/resources/' + resourceId + '/',
        { headers: { 'X-CSRFToken': csrftoken }}
        );
    const deleted = res.data;
    console.log(`Resource deleted!`, deleted);
    // TODO replace refresh with adding dynamically
    location.href = '/';
    return deleted;
      } catch (e) {
        console.error(e);
      }
};

