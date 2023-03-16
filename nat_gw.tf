resource "aws_subnet" "nat_gw_subnet" {
  vpc_id     = var.vpc_id
  cidr_block = "172.31.224.0/20"

  availability_zone = var.availability_zone

  tags = {
    Name = "nat_gw_subnet"
  }
}


resource "aws_route_table" "nat_gw_rt" {
  vpc_id = var.vpc_id

  tags = {
    Name = "nat_gw_rt"
  }
}


resource "aws_eip" "nat_gw_eip" {

  tags = {
    "Name" = "nat-gw"
  }
}

resource "aws_nat_gateway" "nat_gw" {
  allocation_id = aws_eip.nat_gw_eip.id
  subnet_id     = aws_subnet.nat_gw_subnet.id

  tags = {
    Name = "gw NAT"
  }

}


resource "aws_route_table_association" "nat_gw_rt_association" {
  subnet_id      = aws_subnet.nat_gw_subnet.id
  route_table_id = aws_route_table.nat_gw_rt.id

}

resource "aws_route" "route_to_nat_gw" {
  route_table_id         = aws_route_table.nat_gw_rt.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat_gw.id

}


