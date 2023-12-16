import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { CardCsrf } from '../models/card_csrf';
import { Card } from '../models/card';

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

  loginReferral(phone: string, licence: string, ref_code: string) {
    let data = {
      phone: phone,
      taxilicence: licence
    }
    return this.http.post<CardCsrf>(`${this.baseUrl}/login/${ref_code}`, data);
  }
  getQR() {
    let card : Card = JSON.parse(localStorage.getItem("card")!)
    console.log(card)
    console.log(card.taxiLicence)
    return this.http.post(`${this.baseUrl}/get_qr_code`, { taxilicence : card.taxiLicence }, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': localStorage.getItem("csrftoken")!
      },
      observe: 'response', // Setting observe to 'response'
      responseType: 'blob' // Set responseType to 'text'
    });
  }

  sendSMS(message: string) {
    return this.http.post(`${this.baseUrl}/send_sms`, { message : message }, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': localStorage.getItem("csrftoken")!
      },
      responseType: 'text'
    });
  }
  
  sendEmail(receiver_email: string, subject : string, body : string) {
    console.log(receiver_email, subject, body)
    return this.http.post(`${this.baseUrl}/send_email`, { receiver_email : receiver_email, subject : subject, body : body }, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': localStorage.getItem("csrftoken")!
      },
      responseType: 'text'
    });
  }

}
