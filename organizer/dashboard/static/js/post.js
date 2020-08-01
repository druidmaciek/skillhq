const getToken = () => {
  return document.querySelector('#post-form > input').value;
};

// Delete Post
const deletePost = async (postId) => {
    const csrftoken = getToken();
    try {
        const res = await axios.delete('/api/posts/'+ String(postId) + '/',
            { headers: { 'X-CSRFToken': csrftoken }}
            );
        const response = res.data;
        // Todo remove from dom
        location.href = '/discussion/';
        return response;
    } catch (e) {
        console.error(e);
    }
};
