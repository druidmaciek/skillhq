


// send post request
const updateResourcePost = async (payload, resourceId) => {
    const csrftoken = document.querySelector('#details-form > input').value;
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
    const csrftoken = document.querySelector('#details-form > input').value;
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
