import { BASE_URL } from '../config'
import { buildQueryString } from '@/utils';

class BillApis {
  private readonly baseUrl: string;

  constructor() {
    this.baseUrl = BASE_URL + '/api/bills';
  }

  public fetchBills(houseId: number): Promise<Response> {
    return fetch(this.baseUrl + `?${buildQueryString({id: houseId})}`, { method: "GET" });
  }
}

const billApis = new BillApis();
export { billApis };
