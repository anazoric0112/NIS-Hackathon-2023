import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { CardCsrf } from '../models/card_csrf';

@Injectable({
  providedIn: 'root'
})
export class TaxiService {

  constructor(private http: HttpClient) { }

  baseUrl = "http://localhost:8000/taxi"

  login(phone: string, licence: string) {
    let data = {
      phone: phone,
      taxilicence: licence
    }
    return this.http.post<CardCsrf>(`${this.baseUrl}/login`, data);
  }
  getQR(qr: string) {
    return this.http.get<ArrayBuffer>(`${this.baseUrl}/get_qr_code`);
  }
  sendSMS(phone: string) {

  }
  sendEmail(email: string) {

  }

}
