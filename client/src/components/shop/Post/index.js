import React, { Fragment } from "react";
import Layout from "../layout";
import BlogPost from "./BlogPost";


const Post = () => {
  return (
    <Fragment>
    <Layout children={<BlogPost/>} />
  </Fragment>
  );
};

export default Post;
