import axios from "axios";
const apiURL = 'http://127.0.0.1:5000/recommend?user_id';

// Get UserId
const token = localStorage.getItem("jwt");
var userId = NaN;
if (token){
  const tokenParts = token.split('.');
  const decodedPayload = JSON.parse(atob(tokenParts[1]));
  userId = decodedPayload._id;
}

export const getRecommendProduct = async () => {
  try {
    let res = await axios.get(`${apiURL}=${userId}`);
    console.log('res.data', res.data)
    return res.data;
  } catch (error) {
    console.log(error);
  }
};