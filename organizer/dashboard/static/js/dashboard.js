

// example GET request
const BASE_URL = 'https://jsonplaceholder.typicode.com';
const getTodos = async () => {
    try {
        const res = await axios.get(`${BASE_URL}/todos`);

        const todos = res.data;

        console.log("GET: Here's the list of todos", todos);

        return todos;

    } catch (e) {
        console.error(e);
    }
};

// Add Resource Form Submit

const resourceForm = document.querySelector('#add-resource-form');

const formEvent = resourceForm.addEventListener('submit', async event => {
  event.preventDefault();

  const csrfToken = document.querySelector('#add-resource-form > input').value;
  const title = document.getElementById('new-res__title').value;
  const subject = document.getElementById('new-res__subject').value;
  const url = document.getElementById('new-res__url').value;
  const type = document.getElementById('new-res__type').value;


  const resource = {
    csrfToken,
    title,
    subject,
    url,
    type,
  };

  const addedResource = await addResource(resource);
});

const addResource = async resource => {
  try {
    const res = await axios.post('/addResource/', resource);
    const addedResource = res.data;

    console.log(`Added a new Todo!`, addedResource);

    return addedResource;
  } catch (e) {
    console.error(e);
  }
};