import * as React from 'react';
import { useEffect, useState } from 'react';
import { useHistory } from "react-router-dom";
import { get_users } from '../api/getUsers';
import UsersDrawer from '../components/settingSections/DrawerUsers';
import AdminHeader from '../components/settingSections/AdminHeader';
import { useContext } from "react";
import AuthContext from "../context/AuthContext";

export default function Admin() {
  const [users, setUsers] = useState([]);
  const { user, socket } = useContext(AuthContext);
  const username = user.sub
  const history = useHistory();


  useEffect(() => {
    get_users().then(users =>{
      if (Array.isArray(users)){
        setUsers(users);
      }else{
        history.push('/')
      }
    });

    socket.emit('update_joined', username, false);
    
}, []);
  

  return (
    <>
      <AdminHeader/>
      <UsersDrawer
      users ={users}
      />
    </>
  );
}