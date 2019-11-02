<%inherit file="../layout.mako"/>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.17/dist/vue.js"></script>

<div class="title" id="title">
	${project}
</div>

<div style="text-align: center;font-size: 21px;padding-top: 20px;">
	${confirmation_msg}
</div>

<div style="text-align: center;font-size: 21px;padding-top: 20px;">
	Click <a href="/forgot_password">here</a> to reset password.
	Click <a href="/login">here</a> to login.
</div>
