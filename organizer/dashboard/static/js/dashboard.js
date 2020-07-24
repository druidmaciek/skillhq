

// example GET request
const getTasks = async () => {
    try {
        const res = await axios.get('/api/tasks/');

        const tasks = res.data;

        console.log(tasks);

        return tasks;

    } catch (e) {
        console.error(e);
    }
};

// Add Resource Form Submit

const resourceForm = document.querySelector('#add-resource-form');

const formEvent = resourceForm.addEventListener('submit', async event => {
  event.preventDefault();

  const title = document.getElementById('new-res__title').value;
  const subject = document.getElementById('new-res__subject').value;
  const url = document.getElementById('new-res__url').value;
  const resource_type = document.getElementById('new-res__type').value;
  const description = document.getElementById('new-res__description').value;
  let tasks = [];

  var taskElements = document.getElementsByClassName("mtask-item");
    for (var i = 0; i < taskElements.length; i++) {
       const taskElem = taskElements.item(i);
        const title = taskElem.getElementsByClassName('task-title')[0].value;
        let status = taskElem.getElementsByClassName('task-status')[0].value;
        if (status == "true") {
            status = "completed";
        } else {
            status = "todo";
        }
        const task = {
            title,
            status
        }
        tasks.push(task)
    }

  const resource = {
    title,
    subject,
    url,
    resource_type,
    tasks,
    description
  };

  const addedResource = await addResource(resource);
});

const addResource = async resource => {
    const csrftoken = document.querySelector('#add-resource-form > input').value;
  try {
    const res = await axios.post('/api/resources/', resource,
        { headers: { 'X-CSRFToken': csrftoken }}
        );
    const addedResource = res.data;
    console.log(`Added a new Resource!`, addedResource);
    // TODO replace refresh with adding dynamically
    //location.href = '/resource/'+String(addedResource.data.id)+"/";
      location.reload();

    return addedResource;
  } catch (e) {
      location.reload();
    console.error(e);
  }
};