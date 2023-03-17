output "Elastic_IP" {
  value = aws_eip.nat_gw_eip.public_ip

}
