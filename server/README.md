# Reset Admin Account
```sh
curl -X POST --data "{}" http://127.0.0.1:${PORT}/api/v1/reset_admin
```

# Manual Reset Account MFA Secret
```sql
UPDATE d_user_info SET mfa_secret_key=null WHERE username='xxx';
```

# Todo
- [ ] Done setting front and back
- [ ] Crontab for clear log with 6 months
