import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { CardCsrf } from '../models/card_csrf';

@Injectable({
  providedIn: 'root'
})
export class TaxiService {

  constructor(private http: HttpClient) { }

  baseUrl = "http://localhost:8000"

  login(phone: string, licence: string) {
    let data = {
      phone: phone,
      taxilicence: licence
    }
    return this.http.post<CardCsrf>(`${this.baseUrl}/taxi/login`, data);
  }
  scanQR(qr: string) {

  }
  sendSMS(phone: string) {

  }
  sendEmail(email: string) {

  }

}
