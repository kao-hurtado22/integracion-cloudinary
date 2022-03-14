import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

function App() {

  const [state, setState] = useState({
    username: '',
    password: '',
    avatar: null,
    cv: null
  })

  const [user, setUser] = useState(null);


  const handleChange = e => {
    const { name, value } = e.target;
    const newState = { ...state };
    newState[name] = value;
    setState(newState);
  }

  const handleChangeFile = e => {
    const { name, files } = e.target;
    const newState = { ...state };
    newState[name] = files[0];
    setState(newState);
  }

  const handleSubmit = e => {
    e.preventDefault();

    let formData = new FormData();
    formData.append("username", state.username);
    formData.append("password", state.password);
    formData.append("avatar", state.avatar)
    formData.append("cv", state.cv);

    register(e.target, formData);
  }

  const register = (form, formData) => {
    fetch('https://5000-ljavierrodrigue-integrat-iqnbpi7v11t.ws-us34.gitpod.io/api/register', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if(data.id){
          setUser(data);
          setState({
            username: '',
            password: '',
            avatar: null,
            cv: null
          })
          form.reset();

        }else{
          // asignar el mensaje de error
        }
      })
      .catch(error => console.log(error));
  }


  return (
    <div className="container">
      <div className="row">
        <div className="col-md-12 my-5">
          <form onSubmit={handleSubmit}>
            <div className="form-group mb-3">
              <label htmlFor="username">Username</label>
              <input type="email" name="username" id="username" placeholder='john.doe@email.com' onChange={handleChange} className="form-control" value={state.username} />
            </div>
            <div className="form-group mb-3">
              <label htmlFor="password">Password</label>
              <input type="password" name="password" id="password" placeholder='xxxxxxxxx' onChange={handleChange} className="form-control" value={state.password}/>
            </div>
            <div className="form-group mb-3">
              <label htmlFor="username">Avatar</label>
              <input type="file" name="avatar" id="avatar" placeholder='Seleccine avatar' onChange={handleChangeFile} className="form-control" />
            </div>
            <div className="form-group mb-3">
              <label htmlFor="cv">CV</label>
              <input type="file" name="cv" id="cv" placeholder='Seleccione CV' onChange={handleChangeFile} className="form-control" />
            </div>
            <div className="d-grid">
              <button className="btn btn-primary gap-2">
                Registrar
              </button>
            </div>
          </form>
        </div>

        <div className="col-md-12">
          {
            user && (
              <div className="card mb-3" style={{ maxWidth: 540 }}>
                <div className="row g-0">
                  <div className="col-md-4">
                    <img src={user && user.avatar} className="img-fluid rounded-start" alt="avatar" />
                  </div>
                  <div className="col-md-8">
                    <div className="card-body">
                      <h5 className="card-title">{user && user.username}</h5>
                      <p className="card-text">
                        Mi cv <a href={user && user.cv} className="btn btn-warning" target="_blank">Descargar CV</a>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )
          }
        </div>
      </div>
    </div>
  );
}

export default App;
