// Add Note
const addNote = async (title, content) => {

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const resource = urlParams.get('resource');
    const csrftoken = document.querySelector('#details-form > input').value;

    try {
    const res = await axios.post('/api/notes/',
        { title, content, resource },
        { headers: { 'X-CSRFToken': csrftoken }}
        );
    const response = res.data;
    location.href = "/notes/" + String(response.id) + "/"
    return response;
      } catch (e) {
        console.error(e);
      }
};