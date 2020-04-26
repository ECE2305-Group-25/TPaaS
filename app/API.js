const config = require('./config.json');
// NOTE: Make sure the settings in config.json match the configuration needed to connect to your deployed MBSR server.

class API {
  constructor() {
    this.url = `${config.protocol}://${config.host}:${config.port}`;
  }


  async get(path) {
    let call = await (fetch(`${this.url}/api${path}`, {
      method: 'GET',
      credentials: 'same-origin',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    }).catch((err) => ({ success: false, reason: String(err) })));
    if ('success' in call && !call.success) return call;
    if (!call.ok) {
      let json_response = '';
      if ('json' in call) json_response = await call.json();
      if (typeof json_response === 'string') return { success: false, reason: json_response };
      if ('success' in json_response && !json_response.success) return json_response;
      return { error: call.statusText || call.status };
    }

    if (!('json' in call)) return call;

    return call.json().catch((err) => ({ error: err }));
  }

  async get_page(path, page_size, page_number) {
    let url = `${path}?limit=${page_size}&start=${page_number * page_size}`;
    const result = await this.get(url);
    return result;
  }

  async get_status() {
    return this.get('/status');
  }

  async get_generate_pin() {
    return this.get('/generate_pin');
  }

  async get_dispense(auth) {
    return this.get(`/dispense?auth=${auth}`);
  }
}

export default new API();
