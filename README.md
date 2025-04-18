# Multi-Domain Docker Setup

This repository contains the Docker setup and GitHub Actions workflow for multiple applications:
- sWallet application (swallet.me)
- CreateDAO application (createdao.org)

## Project Structure

- `client/`: Next.js application for sWallet
- `Dockerfile`: Docker configuration for the sWallet Next.js application
- `docker-compose.yml`: Docker Compose configuration with Nginx and Certbot for both domains
- `nginx/`: Nginx configuration with Content Security Policy for both domains
- `.github/workflows/`: GitHub Actions workflow for CI/CD

## Local Development

1. Clone the repository
2. Create a `.env` file in the root directory with the following variables:
   ```
   NEXT_PUBLIC_PRIVY_APP_ID=<your-privy-app-id>
   PRIVY_APP_SECRET=<your-privy-app-secret>
   ```
3. Make sure the CreateDAO application is running in its own container
4. Run the deployment script:
   ```
   ./deploy.sh
   ```
   This script will:
   - Check if the `.env` file exists
   - Initialize Let's Encrypt certificates for both domains
   - Build and start the Docker containers
4. Set up your hosts file to map both domains to localhost:
   ```
   sudo ./setup-hosts.sh
   ```
5. Access the applications at:
   - https://swallet.me
   - https://createdao.org

Alternatively, you can run the application manually:
```
# Initialize Let's Encrypt certificates
./init-letsencrypt.sh

# Start the containers
docker-compose up -d
```

## SSL Certificates

This project uses Let's Encrypt for SSL certificates. The certificates are automatically obtained and renewed using Certbot.

For local development, the `init-letsencrypt.sh` script will create dummy certificates for both domains and then attempt to obtain real certificates from Let's Encrypt.

The script is configured to handle certificates for:
- swallet.me and www.swallet.me
- createdao.org and www.createdao.org

Before running in production, make sure to:
1. Verify the `domains` array in `init-letsencrypt.sh` includes all your domain names
2. Add your email address to the `email` variable in `init-letsencrypt.sh` for Let's Encrypt notifications

## Multi-Domain Nginx Configuration

The Nginx configuration is set up to handle multiple domains:

1. **swallet.me**:
   - Proxies requests to the Next.js container on port 3000
   - Uses SSL certificates from Let's Encrypt
   - Includes Content Security Policy for Privy authentication and WalletConnect

2. **createdao.org**:
   - Proxies requests to the CreateDAO container on port 80
   - Uses SSL certificates from Let's Encrypt
   - Includes appropriate security headers

## Docker Networking

The Docker Compose configuration connects the Nginx container to two networks:
- `app-network`: For communication with the sWallet Next.js container
- `dao-network`: For communication with the CreateDAO container

The `dao-network` is configured as an external network, assuming it's created by the CreateDAO application's Docker Compose setup.

## GitHub Actions

The GitHub Actions workflow is configured to:

1. Build the Docker image for sWallet
2. Push the image to GitHub Container Registry (GHCR)
3. Deploy both applications to the production server using docker-compose.prod.yml

### Required Secrets

The following secrets need to be set in the GitHub repository settings:

- `GITHUB_TOKEN`: Automatically provided by GitHub Actions
- `SSH_HOST`: Production server hostname
- `SSH_USERNAME`: Production server username
- `SSH_PRIVATE_KEY`: SSH private key for the production server

### Production Deployment

The production deployment uses a separate docker-compose.prod.yml file that is configured to:

1. Pull the Next.js image from GitHub Container Registry
2. Use Let's Encrypt for SSL certificates
3. Configure Nginx with the specified Content Security Policy

## Content Security Policies

### sWallet (swallet.me)

The Nginx configuration includes a Content Security Policy (CSP) for swallet.me with the following directives:

```
default-src 'self';
script-src 'self' https://challenges.cloudflare.com;
style-src 'self' 'unsafe-inline';
img-src 'self' data: blob:;
font-src 'self';
object-src 'none';
base-uri 'self';
form-action 'self';
frame-ancestors 'none';
child-src https://auth.privy.io https://verify.walletconnect.com https://verify.walletconnect.org;
frame-src https://auth.privy.io https://verify.walletconnect.com https://verify.walletconnect.org https://challenges.cloudflare.com;
connect-src 'self' https://auth.privy.io wss://relay.walletconnect.com wss://relay.walletconnect.org wss://www.walletlink.org https://*.rpc.privy.systems;
worker-src 'self';
manifest-src 'self'
```

This CSP is configured to work with Privy authentication and WalletConnect.

### CreateDAO (createdao.org)

The Nginx configuration includes a Content Security Policy (CSP) for createdao.org with the following directives:

```
default-src 'self' 'unsafe-inline' 'unsafe-eval' data: *.walletconnect.com *.infura.io;
connect-src 'self' *;
```

This CSP is configured to work with the CreateDAO application's requirements.
