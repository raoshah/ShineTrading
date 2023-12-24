import http.client

conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
payload = "{\r\n     \"exchange\": \"NSE\",\r\n \"symboltoken\": \"3045\",\r\n     \"interval\": \"ONE_MINUTE\",\r\n  \"fromdate\": \"2021-02-08 09:00\",\r\n     \"todate\": \"2021-02-08 09:16\"\r\n}"
headers = {
  'X-PrivateKey': 'qATshT3J',
  'Accept': 'application/json',
  'X-SourceID': 'WEB',
  'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
  'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
  'X-MACAddress': 'MAC_ADDRESS',
  'X-UserType': 'USER',
  'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IlM1MDI2MzkiLCJyb2xlcyI6MCwidXNlcnR5cGUiOiJVU0VSIiwidG9rZW4iOiJleUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKemRXSWlPaUpUTlRBeU5qTTVJaXdpWlhod0lqb3hOekF6TlRJM05UVTFMQ0pwWVhRaU9qRTNNRE0wTWpjd01UWXNJbXAwYVNJNkltWXhOelJpWWpZeExXSmhORGt0TkRZNE5DMWlaREF4TFdReFltTmhOek0yTVdSaFpDSXNJbTl0Ym1WdFlXNWhaMlZ5YVdRaU9qTXNJbk52ZFhKalpXbGtJam9pTXlJc0luVnpaWEpmZEhsd1pTSTZJbU5zYVdWdWRDSXNJblJ2YTJWdVgzUjVjR1VpT2lKMGNtRmtaVjloWTJObGMzTmZkRzlyWlc0aUxDSm5iVjlwWkNJNk15d2ljMjkxY21ObElqb2lNeUo5LjJkcm1qMHFQX0dXc2t1VGFXNDdTcF8yZHR0VVRlU3RtaC1aSUoyd0hPVDFrWkk4NUF3TGhXOWVpZlRQMkpNNTE5b0VzZXdGUWlHVnBWak1ic2M4c2F3IiwiQVBJLUtFWSI6InFBVHNoVDNKIiwiaWF0IjoxNzAzNDI3MDc2LCJleHAiOjE3MDM1Mjc1NTV9.V5M5o2Bhp1RFzNl3Ukq1vlNCLvDJvk1JhhTdovIBSXAtMIKBR_T36d4kzXlRiqFLEI8o4DGg-LRpuR77ePAJ9A',
  'Accept': 'application/json',
  'X-SourceID': 'WEB',
  'Content-Type': 'application/json'
}
conn.request("POST", "/rest/secure/angelbroking/historical/v1/getCandleData", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
