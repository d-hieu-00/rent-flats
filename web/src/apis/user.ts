import { BASE_URL } from '../config'

class UserApis {
    private readonly baseUrl: string;

    constructor()
    {
        this.baseUrl = BASE_URL + '/api';
    }

    public fetchUser() : Promise<Response>
    {
        return fetch(this.baseUrl + "/user", { method: "GET" });
    }

    public login(username: string, password: string) : Promise<Response>
    {
        const inBody = JSON.stringify({
            username: username,
            password: password
        })
        return fetch(this.baseUrl + "/login", { method: "POST", body: inBody });
    }

    public logout() : Promise<Response>
    {
        return fetch(this.baseUrl + "/logout", { method: "POST" });
    }
}

const userApis = new UserApis();
export { userApis };
