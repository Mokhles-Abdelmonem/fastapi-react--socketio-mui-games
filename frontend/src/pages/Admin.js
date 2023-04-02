import * as React from 'react';
import { useEffect, useState } from 'react';

import { get_users } from '../api/getUsers';
import UsersDrawer from '../components/settingSections/DrawerUsers';
import AdminHeader from '../components/settingSections/AdminHeader';

export default function Admin() {
  const [users, setUsers] = useState([]);
  
  useEffect(() => {
    get_users().then(users =>{
        setUsers(users);
    })

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