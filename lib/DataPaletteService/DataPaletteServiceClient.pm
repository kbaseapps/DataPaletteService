package DataPaletteService::DataPaletteServiceClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

DataPaletteService::DataPaletteServiceClient

=head1 DESCRIPTION





=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => DataPaletteService::DataPaletteServiceClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my $token = Bio::KBase::AuthToken->new(@args);
	
	if (!$token->error_message)
	{
	    $self->{token} = $token->token;
	    $self->{client}->{token} = $token->token;
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 list_data

  $data_list = $obj->list_data($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a DataPaletteService.ListDataParams
$data_list is a DataPaletteService.DataList
ListDataParams is a reference to a hash where the following keys are defined:
	workspaces has a value which is a reference to a list where each element is a DataPaletteService.ws_name_or_id
ws_name_or_id is a string
DataList is a reference to a hash where the following keys are defined:
	data has a value which is a reference to a list where each element is a DataPaletteService.DataInfo
DataInfo is a reference to a hash where the following keys are defined:
	ref has a value which is a DataPaletteService.ws_ref
	meta has a value which is a string
	src_nar has a value which is a string
ws_ref is a string

</pre>

=end html

=begin text

$params is a DataPaletteService.ListDataParams
$data_list is a DataPaletteService.DataList
ListDataParams is a reference to a hash where the following keys are defined:
	workspaces has a value which is a reference to a list where each element is a DataPaletteService.ws_name_or_id
ws_name_or_id is a string
DataList is a reference to a hash where the following keys are defined:
	data has a value which is a reference to a list where each element is a DataPaletteService.DataInfo
DataInfo is a reference to a hash where the following keys are defined:
	ref has a value which is a DataPaletteService.ws_ref
	meta has a value which is a string
	src_nar has a value which is a string
ws_ref is a string


=end text

=item Description



=back

=cut

 sub list_data
{
    my($self, @args) = @_;

# Authentication: optional

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function list_data (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to list_data:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'list_data');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "DataPaletteService.list_data",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'list_data',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method list_data",
					    status_line => $self->{client}->status_line,
					    method_name => 'list_data',
				       );
    }
}
 


=head2 add_to_palette

  $obj->add_to_palette($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a DataPaletteService.AddToPaletteParams
AddToPaletteParams is a reference to a hash where the following keys are defined:
	workspace has a value which is a DataPaletteService.ws_name_or_id
	new_refs has a value which is a reference to a list where each element is a DataPaletteService.ObjectReference
ws_name_or_id is a string
ObjectReference is a reference to a hash where the following keys are defined:
	ref has a value which is a DataPaletteService.ws_ref
ws_ref is a string

</pre>

=end html

=begin text

$params is a DataPaletteService.AddToPaletteParams
AddToPaletteParams is a reference to a hash where the following keys are defined:
	workspace has a value which is a DataPaletteService.ws_name_or_id
	new_refs has a value which is a reference to a list where each element is a DataPaletteService.ObjectReference
ws_name_or_id is a string
ObjectReference is a reference to a hash where the following keys are defined:
	ref has a value which is a DataPaletteService.ws_ref
ws_ref is a string


=end text

=item Description



=back

=cut

 sub add_to_palette
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function add_to_palette (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to add_to_palette:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'add_to_palette');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "DataPaletteService.add_to_palette",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'add_to_palette',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return;
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method add_to_palette",
					    status_line => $self->{client}->status_line,
					    method_name => 'add_to_palette',
				       );
    }
}
 


=head2 remove_from_palette

  $obj->remove_from_palette($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a DataPaletteService.RemoveFromPaletteParams
RemoveFromPaletteParams is a reference to a hash where the following keys are defined:
	workspace has a value which is a DataPaletteService.ws_name_or_id
	refs has a value which is a reference to a list where each element is a DataPaletteService.ws_ref
ws_name_or_id is a string
ws_ref is a string

</pre>

=end html

=begin text

$params is a DataPaletteService.RemoveFromPaletteParams
RemoveFromPaletteParams is a reference to a hash where the following keys are defined:
	workspace has a value which is a DataPaletteService.ws_name_or_id
	refs has a value which is a reference to a list where each element is a DataPaletteService.ws_ref
ws_name_or_id is a string
ws_ref is a string


=end text

=item Description



=back

=cut

 sub remove_from_palette
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function remove_from_palette (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to remove_from_palette:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'remove_from_palette');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "DataPaletteService.remove_from_palette",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'remove_from_palette',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return;
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method remove_from_palette",
					    status_line => $self->{client}->status_line,
					    method_name => 'remove_from_palette',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "DataPaletteService.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "DataPaletteService.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'remove_from_palette',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method remove_from_palette",
            status_line => $self->{client}->status_line,
            method_name => 'remove_from_palette',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for DataPaletteService::DataPaletteServiceClient\n";
    }
    if ($sMajor == 0) {
        warn "DataPaletteService::DataPaletteServiceClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 ws_ref

=over 4



=item Description

@id ws


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 DataInfo

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ref has a value which is a DataPaletteService.ws_ref
meta has a value which is a string
src_nar has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ref has a value which is a DataPaletteService.ws_ref
meta has a value which is a string
src_nar has a value which is a string


=end text

=back



=head2 DataList

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
data has a value which is a reference to a list where each element is a DataPaletteService.DataInfo

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
data has a value which is a reference to a list where each element is a DataPaletteService.DataInfo


=end text

=back



=head2 ws_name_or_id

=over 4



=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 ListDataParams

=over 4



=item Description

todo: pagination?


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspaces has a value which is a reference to a list where each element is a DataPaletteService.ws_name_or_id

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspaces has a value which is a reference to a list where each element is a DataPaletteService.ws_name_or_id


=end text

=back



=head2 ObjectReference

=over 4



=item Description

todo: allow passing in a reference chain


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ref has a value which is a DataPaletteService.ws_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ref has a value which is a DataPaletteService.ws_ref


=end text

=back



=head2 AddToPaletteParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace has a value which is a DataPaletteService.ws_name_or_id
new_refs has a value which is a reference to a list where each element is a DataPaletteService.ObjectReference

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace has a value which is a DataPaletteService.ws_name_or_id
new_refs has a value which is a reference to a list where each element is a DataPaletteService.ObjectReference


=end text

=back



=head2 RemoveFromPaletteParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
workspace has a value which is a DataPaletteService.ws_name_or_id
refs has a value which is a reference to a list where each element is a DataPaletteService.ws_ref

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
workspace has a value which is a DataPaletteService.ws_name_or_id
refs has a value which is a reference to a list where each element is a DataPaletteService.ws_ref


=end text

=back



=cut

package DataPaletteService::DataPaletteServiceClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
