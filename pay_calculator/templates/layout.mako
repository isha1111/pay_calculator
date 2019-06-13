<!DOCTYPE html>
<html lang="${request.locale_name}">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vue@2.5.17/dist/vue.js"></script>
    <title>Pay Calculator</title>
    <link rel="icon" href="data:,">
    <link rel="stylesheet" type="text/css" href="/static/css/index.css">
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.js"></script>
  </head>

  <body>
      <div class="header_top">
          % if username != '':
          <span class="menu_option"> <a href="/logout" style="color: #ffffff;text-decoration: none;">Logout</a></span>
          % endif 
        </div>
        ${ next.body() }
        <div class="footer">
          <span class="company">© 2019 JMD Facilty Services. All Rights Reserved.</span>
          <span class="creator">Created By Isha Nagpal</span>
        </div>
  </body>
</html>
<script type="text/javascript">
  
</script>

