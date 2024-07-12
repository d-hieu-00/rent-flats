import { BASE_URL } from '../config'
import { buildQueryString } from '@/utils';

class HouseApis {
  private readonly baseUrl: string;

  constructor() {
    this.baseUrl = BASE_URL + '/api/houses';
  }

  public fetchHouses(params: any): Promise<Response> {
    return fetch(this.baseUrl + `?${buildQueryString(params)}`, { method: "GET" });
  }
}

const houseApis = new HouseApis();
export { houseApis };
