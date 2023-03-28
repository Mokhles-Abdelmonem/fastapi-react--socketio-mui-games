function UserInfo({ user }) {
    return (
      <div>
        <h1>Hello, {user.sub}</h1>
      </div>
    );
  }
  
  export default UserInfo;